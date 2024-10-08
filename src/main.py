from fastapi import FastAPI
from user.api import router as user_router


app = FastAPI(title="FastAPI Async")
app.include_router(user_router)


@app.get("/")
async def root_handler():
    return {"ping": "pong"}
