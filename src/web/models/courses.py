import sqlalchemy
from sqlalchemy import orm

from models.db_session import SqlAlchemyBase


class Course(SqlAlchemyBase):
    __tablename__ = 'courses'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)

    students = orm.relationship("Student", back_populates='course')
