import sqlalchemy
from sqlalchemy import orm

from db_models.db_session import SqlAlchemyBase


class Student(SqlAlchemyBase):
    __tablename__ = 'students'


    __table_args__ = (
        # this can be db.PrimaryKeyConstraint if you want it to be a primary key
        sqlalchemy.UniqueConstraint('system_id', 'course_id'),
      )
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    system_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    
    course_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("courses.id"))
    course = orm.relationship('Course', back_populates='students')

    feedbacks = orm.relationship("Feedback", back_populates='students')
