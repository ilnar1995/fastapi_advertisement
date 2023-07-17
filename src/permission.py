from functools import wraps
from fastapi import HTTPException

def owner_or_superuser_access(model_param_name, user_param_name):
    """
    У функции должны присуствовать два параметра 'user' и 'model_name'
    Проверяется равенство 'model_name.advertisement == user.id'
    при несовпадении выдает ошибку отсутствия доступа
    """
    def decor(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            advertisement = kwargs.get(model_param_name)
            user = kwargs.get(user_param_name)
            if advertisement.user.id != user.id and not user.is_superuser:
                raise HTTPException(status_code=401, detail="You have no access")
            return await func(*args, **kwargs)
        return wrapper
    return decor

def not_banned_access(func):
    """
    Проверка забанен ли пользователь
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        user = kwargs.get('user')
        if user.is_banned:
            raise HTTPException(status_code=401, detail="You profile is banned")
        return await func(*args, **kwargs)
    return wrapper

def superuser_access(func):
    """
    Проверка прав суперпользователя
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        user = kwargs.get('user')
        if not user.is_superuser:
            raise HTTPException(status_code=401, detail="You need superuser access")
        return await func(*args, **kwargs)
    return wrapper