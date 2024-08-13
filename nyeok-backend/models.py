from pydantic import BaseModel


class User(BaseModel):
    uid: int
    username: str
    hashed_password: str
