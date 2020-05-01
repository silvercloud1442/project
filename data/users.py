import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String)
    surname = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String)
    age = sqlalchemy.Column(sqlalchemy.Integer)
    description = sqlalchemy.Column(sqlalchemy.String)
    rating = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    works = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    worker = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    img = sqlalchemy.Column(sqlalchemy.String, default='/static/img/guest_img.jpg')

    hassed_password = sqlalchemy.Column(sqlalchemy.String)

    def set_password(password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hassed_password, password)
