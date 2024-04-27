import sqlalchemy
from sqlalchemy import orm

from db_models.db_session import SqlAlchemyBase


class Feedback(SqlAlchemyBase):
    __tablename__ = 'feedbacks'

    
    __table_args__ = (
        sqlalchemy.UniqueConstraint('answers', 'student_id'),
      )
    
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    answers = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    student_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("students.id"))
    students = orm.relationship('Student', back_populates='feedbacks')
