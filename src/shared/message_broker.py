import asyncio
import json
from typing import TypedDict, ClassVar

from redis.asyncio import Redis as AsyncRedis
from redis.asyncio.client import PubSub

from shared.config import settings
from shared.websocket import ws_manager


class MessagePayload(TypedDict):
    client_id: int
    message: str


class MessageBroker:
    CHANNEL_NAME: ClassVar[str] = "openchat"

    def __init__(self):
        self.client = AsyncRedis(host=settings.redis_host, port=settings.redis_port, db=0, decode_responses=True)

    @classmethod
    def init(cls):
        broker = cls()
        asyncio.ensure_future(broker._subscribe())
        return broker

    async def publish(self, client_id: int, message: str):
        payload: MessagePayload = MessagePayload(client_id=client_id, message=message)
        await self.client.publish(channel=self.CHANNEL_NAME, message=json.dumps(payload))

    async def _subscribe(self):
        pubsub: PubSub = self.client.pubsub()
        await pubsub.subscribe(self.CHANNEL_NAME)
        asyncio.ensure_future(self._read_message(pubsub=pubsub))

    @staticmethod
    async def _read_message(pubsub: PubSub):
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True)
            if message is not None:
                payload: MessagePayload = json.loads(message['data'])
                await ws_manager.broadcast(sender_client_id=payload["client_id"], message=payload["message"])


# message_broker = MessageBroker.init()
