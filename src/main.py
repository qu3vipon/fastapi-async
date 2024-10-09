from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from shared.config import settings
from user.api import router as user_router


app = FastAPI(title="FastAPI Async")
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.app_secret_key,
)

app.include_router(user_router)


@app.get("/")
async def root_handler():
    return {"ping": "pong"}
