import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_sess import SqlAlchemyBase


class Files(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Files'

    name = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    path = sqlalchemy.Column(sqlalchemy.String, nullable=True)