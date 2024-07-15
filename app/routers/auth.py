from __future__ import annotations
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field, field_validator
from sqlalchemy.orm import Session

from database import user_crud
from database.db import get_db
from database.records import UserRecord
from models import User

router = APIRouter(prefix="/user")


# We should make /auth directory and seperate business logic?
class SignupForm(BaseModel):
    username: str = Field(..., min_length=1, max_length=20)
    plain_password: str

    @field_validator("plain_password")
    def password_must_be_long(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError(
                "Password must be at least 8 characters long",
            )
        return value


def user_record_to_user(user: UserRecord) -> User:
    return User(
        uid=user.uid, username=user.username, hashed_password=user.hashed_password
    )


@router.post("/signup")
async def signup(new_user: SignupForm, db: Session = Depends(get_db)) -> str:
    # Basic input validation by pydantic

    print(new_user.plain_password)
    if user_crud.read_by_username(db, new_user.username) is not None:
        return "User already exists!"

    # Create a new user
    user = UserRecord(
        username=new_user.username, hashed_password=f"##{new_user.plain_password}"
    )
    user_crud.create(db, user)

    return "User signed up!"


@router.get("/test/all_users")
async def test_all_users(db: Session = Depends(get_db)) -> list[User]:
    return list(map(user_record_to_user, user_crud.read_all(db)))
