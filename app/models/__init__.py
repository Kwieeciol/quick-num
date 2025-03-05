from tortoise import Model
from tortoise.fields import (
    IntField,
    TextField,
    CharField,
    ForeignKeyField,
    ForeignKeyRelation,
    DatetimeField
)

__all__ = ('User', 'Balance', 'Transactions')


class User(Model):
    id: int = IntField(primary=True)
    username: CharField = CharField(max_length=64)
    password: str = TextField()
    email: str = TextField()


class Balance(Model):
    id: int = IntField(primary=True)
    user_id: ForeignKeyRelation[User] = ForeignKeyField('models.User', related_name='id')
    amount: int = IntField()
    currency: CharField = CharField(max_length=8)


class Transactions(Model):
    id: int = IntField(primary=True)
    user_id: ForeignKeyRelation[User] = ForeignKeyField('models.User', related_name='id')
    amount: int = IntField()
    currency: CharField = CharField(max_length=8)
    timestamp: DatetimeField = DatetimeField(auto_now=True)
