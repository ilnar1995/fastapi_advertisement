from pydantic import BaseModel, validator, Field
from datetime import datetime
from .models import type_of_advertisement



class AdvertisementCreate(BaseModel):
    type: str = Field(..., example="продажа")
    title: str
    description: str = 'default description'

    @validator("type", pre=True)
    def toppings_validate(cls, date):
        if date not in type_of_advertisement:
            raise ValueError('passwords do not match')
        return date


class AdvertisementList(AdvertisementCreate):
    id: int
    create_at: datetime
    user: str

    @validator("user", pre=True)
    def toppings_validate(cls, date):
        return str(date.get('id'))

class CommentCreate(BaseModel):
    text: str


class CommentList(CommentCreate):
    id: int
    create_at: datetime
    user: str
    advertisement: int

    @validator("user", pre=True)
    def user_validate(cls, date):
        return str(date.get('id'))

    @validator("advertisement", pre=True)
    def advertisement_validate(cls, date):
        return date.get('id')
