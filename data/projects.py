import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Projects(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'projects'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    author = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    title = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    img = sqlalchemy.Column(sqlalchemy.String, default='\\static\\projects_img\\void_img.jpg')
    user = orm.relation('User')