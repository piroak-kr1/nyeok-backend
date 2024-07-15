from __future__ import annotations
from fastapi import APIRouter

from auth.signup import SignupForm

router = APIRouter(prefix="/user")


@router.post("/signup")
async def signup(new_user: SignupForm):
    # Basic input validation by pydantic

    return "User signed up!"
