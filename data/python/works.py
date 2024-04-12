import sqlalchemy
from data.python.db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from . import db_session


class Works(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'works'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))

    type_works = sqlalchemy.Column(sqlalchemy.String)

    name_file = sqlalchemy.Column(sqlalchemy.String)

    user = orm.relationship('User')


def add_works(user_id, type_works, name_file):
    works = Works(user_id=user_id,
                  type_works=type_works,
                  name_file=name_file)
    db_sess = db_session.create_session()
    db_sess.add(works)
    db_sess.commit()
