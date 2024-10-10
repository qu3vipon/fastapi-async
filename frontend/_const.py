from enum import StrEnum


SERVER_URL = "http://backend:8000"
WEBSOCKET_URL = "ws://backend:8000"


class Page(StrEnum):
    HOME = "home.py"
    SIGNUP = "pages/signup.py"
    CHAT = "pages/chat.py"
