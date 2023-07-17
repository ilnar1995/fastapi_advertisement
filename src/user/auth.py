from typing import Optional

from fastapi_users import FastAPIUsers
from fastapi import Request

from src.config import SECRET_AUTH
from src.user.models import user_db
from src.user.schemas import User, UserDB, UserCreate, UserUpdate
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy
from fastapi_users import BaseUserManager


class UserManager(BaseUserManager[UserCreate, UserDB]):
    user_db_model = UserDB
    reset_password_token_secret = SECRET_AUTH
    verification_token_secret = SECRET_AUTH

    async def on_after_request_verify(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")

    async def create_default_user(
            self
    ):
        default_user_email = "default@example.com"
        default_user_password = '1234'
        hashed_password = self.password_helper.hash(default_user_password)
        user_dict = {"email": default_user_email, 'is_superuser': True}
        db_user = self.user_db_model(**user_dict, hashed_password=hashed_password)
        aaa = await self.user_db.get_by_email(default_user_email)
        if not aaa:
            await self.user_db.create(db_user)


async def get_user_manager():
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_AUTH, lifetime_seconds=6600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers(
    get_user_manager,
    [auth_backend],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)

current_active_user = fastapi_users.current_user(active=True)
