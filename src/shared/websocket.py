from fastapi import WebSocket


class WebsocketConnectionManager:
    def __init__(self):
        self.connections: list[tuple[WebSocket, int]] = []

    async def connect(self, websocket: WebSocket, client_id: int):
        await websocket.accept()
        self.connections.append((websocket, client_id))

    def disconnect(self, websocket: WebSocket, client_id):
        self.connections.remove((websocket, client_id))

    async def broadcast(self, sender_client_id: int, message: str):
        for connection, client_id in self.connections:
            if client_id == sender_client_id:
                await connection.send_text(f"<Me>{message}")
            else:
                await connection.send_text(f"<Them>#{str(sender_client_id)[-4:]}: {message}")


ws_manager = WebsocketConnectionManager()
