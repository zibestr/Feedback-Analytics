import sqlalchemy
from db_models.db_session import SqlAlchemyBase
from flask_login import UserMixin


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    nick_name = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    type = sqlalchemy.Column(sqlalchemy.CHAR, nullable=False)
    """ 0 - admin
        1 - teacher
        2 - methodist """
    
    password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    salt = sqlalchemy.Column(sqlalchemy.String, nullable=False)
