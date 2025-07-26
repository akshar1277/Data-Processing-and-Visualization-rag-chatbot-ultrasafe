from pydantic import BaseModel, EmailStr, Field


class AuthSignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    confirm_password: str = Field(min_length=6)


class AuthLoginRequest(BaseModel):
    email: EmailStr
    password: str
