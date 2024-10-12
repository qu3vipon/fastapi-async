import asyncio
import time
from contextlib import asynccontextmanager
from typing import Iterator

import anyio
from fastapi import FastAPI, WebSocket
from starlette.responses import HTMLResponse
from starlette.websockets import WebSocketDisconnect

from shared.chat import html

# from shared.message_broker import message_broker
from shared.websocket import ws_manager
from user.async_api import router as user_async_router
from user.sync_api import router as user_sync_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> Iterator[None]:
    limiter = anyio.to_thread.current_default_thread_limiter()
    limiter.total_tokens = 200
    yield


app = FastAPI(title="FastAPI Async", lifespan=lifespan)
app.include_router(router=user_sync_router, prefix="/sync")
app.include_router(router=user_async_router, prefix="/async")


@app.get("/chats", include_in_schema=False)
async def chats_handler():
    return HTMLResponse(html)


@app.websocket("/ws/{client_id}")
async def websocket_handler(websocket: WebSocket, client_id: int):
    await ws_manager.connect(websocket, client_id)
    try:
        while True:
            message = await websocket.receive_text()
            await ws_manager.broadcast(sender_client_id=client_id, message=message)
            # await message_broker.publish(client_id=client_id, message=message)
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, client_id)


@app.get("/sync/sleep", include_in_schema=False)
def get_sleep_handler():
    time.sleep(1)
    return True


@app.get("/async/sleep", include_in_schema=False)
async def get_async_sleep_handler():
    await asyncio.sleep(1)
    return True
