import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_sess import SqlAlchemyBase


class Files(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'files'

    name = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    path = sqlalchemy.Column(sqlalchemy.String)