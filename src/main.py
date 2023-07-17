import uuid

from fastapi import FastAPI, Depends

from src.routes import routes
from src.core.db import database, metadata, engine
from src.user import models
from src.user.auth import get_user_manager

app = FastAPI()

metadata.create_all(engine)
app.state.database = database


@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()
    user_manager = get_user_manager()
    async for manager in user_manager:
        await manager.create_default_user()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()


app.include_router(routes)
