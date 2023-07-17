from fastapi import APIRouter
from src.user.routers import user_router, auth_router
from src.advertisement.router import advertisement_router


routes = APIRouter()

routes.include_router(auth_router)

routes.include_router(
    advertisement_router,
    prefix="/advertisement",
    tags=["advertisement"],
)

routes.include_router(
    user_router,
    prefix="/user",
    tags=["user"],
)



