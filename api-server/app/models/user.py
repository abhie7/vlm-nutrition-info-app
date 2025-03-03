from pydantic import BaseModel
from beanie import Document


class UserBase(BaseModel):
    email: str
    display_name: str


class UserCreate(UserBase):
    password: str


class User(Document):
    username: str
    email: str
    hashed_password: str

    class Settings:
        collection = "users"
