import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from data.python.db_session import SqlAlchemyBase
from flask_wtf import FlaskForm
from wtforms import EmailField, SubmitField, PasswordField, BooleanField, StringField
from wtforms.validators import DataRequired
from flask_login import UserMixin
from datetime import datetime


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    login = sqlalchemy.Column(sqlalchemy.String)

    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True)

    hashed_password = sqlalchemy.Column(sqlalchemy.String)

    is_premium = sqlalchemy.Column(sqlalchemy.Boolean)

    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.now)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    login = StringField('Имя пользователя', validators=[DataRequired()])
    submit = SubmitField('Войти')