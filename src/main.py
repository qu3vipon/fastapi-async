from fastapi import FastAPI, Request, status
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import JSONResponse

from shared.authentication.session import InvalidSessionKeyError
from shared.config import settings
from user.api import router as user_router


app = FastAPI(title="FastAPI Async")
app.add_middleware(SessionMiddleware, secret_key=settings.app_secret_key)
app.include_router(user_router)


@app.exception_handler(InvalidSessionKeyError)
async def invalid_session_key_error_handler(_: Request, exc: InvalidSessionKeyError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"message": exc.message},
    )


@app.get("/")
async def root_handler():
    return {"ping": "pong"}
