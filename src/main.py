from fastapi import FastAPI, WebSocket
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse
from starlette.websockets import WebSocketDisconnect

from shared.config import settings
from user.api import router as user_router

app = FastAPI(title="FastAPI Async")
app.add_middleware(SessionMiddleware, secret_key=settings.app_secret_key)
app.include_router(user_router)


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
        <style>
        #messages {
            list-style-type: none;
            padding: 0;
            margin: 0;
            display: flex;
            flex-direction: column;
        }

        li {
            margin: 5px 0;
            max-width: 80%;
            border-radius: 10px;
            padding: 10px;
            color: #fff;
        }

        .my-message {
            align-self: flex-end;
            background-color: #007bff;
        }

        .other-message {
            align-self: flex-start;
            background-color: #6c757d;
        }
    </style>
    </head>
    <body>
        <div class="container">
          <h1 class="mt-5">💬 오픈 채팅</h1>
          <hr>
        <h5 class="mt-3">My ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
        <div class="input-group mb-3">
            <input class="form-control" type="text" id="messageText" autocomplete="off"/ placeholder="메시지를 입력하세요..">
            <button class="btn btn-dark">보내기</button>
        </div>
            
        </form>
        <ul id='messages'>
        </ul>
        </div>
        
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id
            var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages');
                var message = document.createElement('li');
    
                if (event.data.startsWith("<Me>")) {
                    var content = document.createTextNode(event.data.replace("<Me>", ""));
                    message.classList.add('my-message');
                } else {
                    var content = document.createTextNode(event.data.replace("<Them>", ""));
                    message.classList.add('other-message');
                }
                
                message.appendChild(content);
                messages.appendChild(message);
        };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


class WebsocketConnectionManager:
    def __init__(self):
        self.connections: list[tuple[WebSocket, int]] = []

    async def connect(self, websocket: WebSocket, client_id: int):
        await websocket.accept()
        self.connections.append((websocket, client_id))

    def disconnect(self, websocket: WebSocket, client_id):
        self.connections.append((websocket, client_id))

    async def broadcast(self, sender_client_id: int, message: str):
        for connection, client_id in self.connections:
            if client_id == sender_client_id:
                await connection.send_text(f"<Me>{message}")
            else:
                await connection.send_text(f"<Them>#{str(sender_client_id)[-4:]}: {message}")


manager = WebsocketConnectionManager()


@app.websocket('/ws/{client_id}')
async def websocket_handler(websocket: WebSocket, client_id: int):
    await manager.connect(websocket, client_id)
    try:
        while True:
            message = await websocket.receive_text()
            await manager.broadcast(sender_client_id=client_id, message=message)
    except WebSocketDisconnect:
        manager.disconnect(websocket, client_id)
