from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from starlette.requests import Request
from fastapi import Depends
from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER


SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

import databases
import ormar
import sqlalchemy


metadata = sqlalchemy.MetaData()
database = databases.Database(SQLALCHEMY_DATABASE_URL)
engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URL)

# Dependency
# вовращаем перемен db из request
# def get_db_session(request: Request):
#     return request.state.db

class MainMata(ormar.ModelMeta):
    metadata = metadata
    database = database

