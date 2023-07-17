import uuid
from typing import Optional

import ormar
from fastapi_users.db import OrmarBaseUserModel, OrmarUserDatabase

from src.core.db import MainMata
from src.user.schemas import UserDB
from typing import ForwardRef

UserRef = ForwardRef("User")


# class UserModerator(ormar.Model):
#     class Meta(MainMata):
#         tablename = "users_moderators"
#
#     id: int = ormar.Integer(primary_key=True)
#
#
# class UserBan(ormar.Model):
#     class Meta(MainMata):
#         tablename = "users_ban"
#
#     id: int = ormar.Integer(primary_key=True)
#

class User(OrmarBaseUserModel):
    class Meta(MainMata):
        tablename = "user"

    id = ormar.UUID(primary_key=True, uuid_format="string", default=uuid.uuid4())
    email = ormar.String(index=True, unique=True, nullable=False, max_length=255)
    hashed_password = ormar.String(nullable=False, max_length=255)
    is_active = ormar.Boolean(default=True, nullable=False)
    is_superuser = ormar.Boolean(default=False, nullable=False)
    is_verified = ormar.Boolean(default=False, nullable=False)
    is_banned = ormar.Boolean(default=False, nullable=False)


User.update_forward_refs()

user_db = OrmarUserDatabase(UserDB, User)
