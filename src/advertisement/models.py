import datetime
import ormar
from typing import Optional, Union, Dict, List
from src.core.db import MainMata

from src.user.models import User

type_of_advertisement = ["продажа", "покупка", "оказание услуг"]

class Advertisement(ormar.Model):
    class Meta(MainMata):
        pass

    id: int = ormar.Integer(primary_key=True)
    type: str = ormar.String(max_length=50, choices=type_of_advertisement)
    title: str = ormar.String(max_length=50)
    description: str = ormar.String(max_length=500)
    create_at: datetime.datetime = ormar.DateTime(default=datetime.datetime.now)
    user: Optional[Union[User, Dict]] = ormar.ForeignKey(User, related_name="user_advertisements")


class Comment(ormar.Model):
    class Meta(MainMata):
        pass

    id: int = ormar.Integer(primary_key=True)
    text: str = ormar.String(max_length=500)
    create_at: datetime.datetime = ormar.DateTime(default=datetime.datetime.now)
    advertisement: Optional[Advertisement] = ormar.ForeignKey(Advertisement, related_name="advertisement_comments",
                                                              ondelete='CASCADE')
    user: Optional[Union[User, Dict]] = ormar.ForeignKey(User, related_name="user_comments")
