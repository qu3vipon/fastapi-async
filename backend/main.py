from fastapi import FastAPI, WebSocket
from starlette.middleware.sessions import SessionMiddleware

from shared.config import settings
from user.api import router as user_router
from chat.api import router as chat_router

app = FastAPI(title="FastAPI Async")
app.add_middleware(SessionMiddleware, secret_key=settings.app_secret_key)
app.include_router(user_router)
app.include_router(chat_router)


@app.get("/")
async def root_handler():
    return {"ping": "pong"}


@app.websocket('/ws')
async def websocket_handler(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
