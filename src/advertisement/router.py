from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request, Path
from src.user.auth import current_active_user
from . import schemas
from . import models
from src.core.db import database
from src.permission import superuser_access, not_banned_access, owner_or_superuser_access
from src.advertisement import services
from functools import wraps
from src.user.auth import fastapi_users
from ..user.models import User

advertisement_router = APIRouter()

# получение объявления по id
async def get_advertisement_by_id(advertisement_id: int = Path(...)):
    advertisement = await models.Advertisement.objects.select_related('user').get_or_none(id=advertisement_id)
    if not advertisement:
        raise HTTPException(status_code=404, detail="No match advertisement")
    return advertisement

# получение сообщения по id
async def get_comment_by_id(comment_id: int = Path(...), advertisement_id: int = Path(...)):
    comment = await models.Comment.objects.get_or_none(id=comment_id, advertisement=advertisement_id)
    if not comment:
        raise HTTPException(status_code=404, detail="No match advertisement")
    return comment


@advertisement_router.get('/', response_model=List[schemas.AdvertisementList])
@not_banned_access
async def get_posts(user: models.User = Depends(current_active_user)):
    advertisements = await models.Advertisement.objects.all()
    return advertisements


@advertisement_router.get('/{advertisement_id}', response_model=schemas.AdvertisementList)
@not_banned_access
async def get_post(
        user: models.User = Depends(current_active_user),
        advertisement: schemas.AdvertisementList = Depends(get_advertisement_by_id)
):
    return advertisement


@advertisement_router.post('/', status_code=201, response_model=schemas.AdvertisementList)
@not_banned_access
async def add_post(
        schema: schemas.AdvertisementCreate,
        user: models.User = Depends(current_active_user)
):
    current_user = await models.User.objects.get(id=user.id)
    return await models.Advertisement.objects.create(title=schema.title, type=schema.type,
                                                     description=schema.description,
                                                     user=current_user)


@database.transaction()
@advertisement_router.delete('/{advertisement_id}')
@owner_or_superuser_access(model_param_name='advertisement', user_param_name='user')
@not_banned_access
async def delete_posts(
        user: models.User = Depends(current_active_user),
        advertisement: schemas.AdvertisementList = Depends(get_advertisement_by_id)
):
    await advertisement.advertisement_comments.clear(keep_reversed=False)
    await advertisement.delete()
    return {'status': 'succsess'}


@advertisement_router.get('/{advertisement_id}/comment', response_model=List[schemas.CommentList])
@not_banned_access
async def get_comments(advertisement_id: int, user: models.User = Depends(current_active_user)):
    comments = await models.Comment.objects.filter(advertisement=advertisement_id).all()
    return comments


@advertisement_router.post('/{advertisement_id}comment', status_code=201, response_model=schemas.CommentList)
@not_banned_access
async def add_comment(
        advertisement_id: int,
        schema: schemas.CommentCreate,
        user: models.User = Depends(current_active_user)
):
    try:
        advertisement = await models.Advertisement.objects.get(id=advertisement_id)
        return await models.Comment.objects.create(text=schema.text, user=user.id, advertisement=advertisement.id)
    except:
        raise HTTPException(status_code=404, detail="No match advertisement")


@advertisement_router.delete('/{advertisement_id}/comment/{comment_id}')
@owner_or_superuser_access(model_param_name='comment', user_param_name='user')
@not_banned_access
async def delete_comment(comment = Depends(get_comment_by_id), user: models.User = Depends(current_active_user)):
    if comment.user.id == user.id or user.is_superuser:
        await comment.delete()
        return {'status': 'succsess'}
