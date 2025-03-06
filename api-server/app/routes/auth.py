import uuid
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from datetime import timedelta
from app.utils.object_to_str import object_id_to_str
from app.services import auth_service
from app.database.user_repository import UserRepository
from app.models.user import UserCreate

router = APIRouter(tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


class Token(BaseModel):
    # access_token: str
    # token_type: str
    user: dict


class LoginPayload(BaseModel):
    email: str
    password: str


class RegisterPayload(BaseModel):
    email: str
    password: str
    display_name: str


@router.post("/login", response_model=Token)
async def login(payload: LoginPayload):
    user_repo = UserRepository()
    user = await user_repo.find_one({"email": payload.email})

    if not user or not auth_service.verify_password(payload.password, user["password"]):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # access_token_expires = timedelta(minutes=30)
    # access_token = auth_service.create_access_token(
    #     data={"sub": user["email"]},
    #     expires_delta=access_token_expires,
    # )

    return {"user": object_id_to_str(user)}


@router.post("/register")
async def register(payload: RegisterPayload):
    user_repo = UserRepository()
    user = await user_repo.find_one({"email": payload.email})

    if user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )

    user_create = UserCreate(
        uuid=str(uuid.uuid4()),
        email=payload.email,
        password=payload.password,
        display_name=payload.display_name,
    )
    await user_repo.create_user(user_create)

    return {
        "message": "User registered successfully",
        "user": object_id_to_str(user_create),
    }


@router.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    user_repo = UserRepository()
    user = await user_repo.find_one({"email": token})
    return user
