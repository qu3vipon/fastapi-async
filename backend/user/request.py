from pydantic import BaseModel, Field


class UserAuthRequest(BaseModel):
    username: str = Field(..., examples=["admin"])
    password: str = Field(..., examples=["1234"])
