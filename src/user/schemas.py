from fastapi_users import models
from pydantic import EmailStr, BaseModel


class User(models.BaseUser):
    pass
    is_banned: bool


class UserCreate(models.CreateUpdateDictModel):
    # username: str
    email: EmailStr
    password: str


class UserUpdate(User, models.BaseUserUpdate):
    pass


class UserDB(User, models.BaseUserDB):
    is_banned: bool = False



