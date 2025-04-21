import uuid
from typing import Optional
from fastapi import Depends, Request,HTTPException
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin, models
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from jose import jwt, JWTError,ExpiredSignatureError
from app.db import get_user_db
from app.schemas import User

SECRET = "SECRET"
ALGORITHMS = ["HS256"]
AUDIENCE= "aiso"
class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="api/v1/login")


# def get_jwt_strategy() -> JWTStrategy[models.UP, models.ID]:
#     return JWTStrategy(secret=SECRET, lifetime_seconds=36000,audience="aiso")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=SECRET,
        lifetime_seconds=36000,
        token_audience="aiso"
    )
    
def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET,
            algorithms=["HS256"],
            audience="aiso"
        )
        return payload
    except JWTError as e:
        raise HTTPException(401, detail=str(e))

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)