import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_sess import SqlAlchemyBase


association_table = sqlalchemy.Table(
    'groups_to_users',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('user', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('group', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('groups.id'))
)


class Groups(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'groups'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    github = sqlalchemy.Column(sqlalchemy.String, nullable=True)