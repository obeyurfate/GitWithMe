import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_sess import SqlAlchemyBase


class Groups(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Groups'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    participants = sqlalchemy.Column(sqlalchemy.String, nullable=True)