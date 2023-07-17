from fastapi import APIRouter, Depends

from src.permission import superuser_access
from src.user import schemas, models
from src.user.auth import auth_backend, fastapi_users, SECRET_AUTH, current_active_user

auth_router = APIRouter()

auth_router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
auth_router.include_router(
    fastapi_users.get_register_router(), prefix="/auth", tags=["auth"]
)
# user_router.include_router(
#     fastapi_users.get_reset_password_router(
#         SECRET, after_forgot_password=on_after_forgot_password
#     ),
#     prefix="/auth",
#     tags=["auth"],
# )
# user_router.include_router(
#     fastapi_users.get_verify_router(
#     ),
#     prefix="/auth",
#     tags=["auth"],
# )
# user_router.include_router(
#     fastapi_users.get_users_router(),
#     prefix="/users",
#     tags=["users"]
# )
user_router = APIRouter()

@user_router.post('/{id}/ban', status_code=201)
@superuser_access
async def ban(
        id: str,
        is_banned: bool = False,
        user: models.User = Depends(current_active_user)
):
    """
    добавление или удаление пользователя в бан пользователя по id
    """
    try:
        await models.User.objects.filter(id=id).update(is_banned=is_banned)
    except:
        return {'error': "error"}
    return {'status': "seccess"}

@user_router.post('/{id}/set_superuser_access', status_code=201)
@superuser_access
async def set_superuser_access(
        id: str,
        is_superuser: bool = False,
        user: models.User = Depends(current_active_user)
):
    """
    добавление или удаление прав суперпользователя для пользователя по id
    """
    try:
        await models.User.objects.filter(id=id).update(is_superuser=is_superuser)
    except:
        return {'error': "error"}
    return {'status': "seccess"}
