from pydantic import BaseModel, Field, EmailStr


class SLogin(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)


class SRegister(SLogin):
    username: str = Field(...)
