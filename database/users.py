import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_sess import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    token = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    nickname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    groups = orm.relation("Group",
                              secondary="groups_to_users",
                              backref="user")