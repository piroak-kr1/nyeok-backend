from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator

import response_code


class SignupForm(BaseModel):
    username: str = Field(..., min_length=1, max_length=20)
    plain_password: str

    @field_validator("plain_password")
    def password_must_be_long(cls, value: str) -> None:
        if len(value) < 8:
            raise HTTPException(
                response_code.Unprocessable_Content,
                detail="Password must be at least 8 characters long",
            )
