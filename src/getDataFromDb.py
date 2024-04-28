import os
from sqlalchemy import select
from db_models import db_session
import json
from db_models.courses import Course
from db_models.students import Student
from db_models.feedbacks import Feedback
import pandas


def getData():
    db_session.global_init(os.path.abspath('db/database.sqlite3'))
    session = db_session.create_session()

    statement = select(Feedback).order_by(Feedback.id.desc())
    user_obj = session.scalars(statement).fetchmany(100)

    res = []
    for i in user_obj:
        i.answers = i.answers.replace("\"", '\\"')
        i.answers = i.answers.replace("'", '"')
        data = json.loads(i.answers)
        t = []
        statement = select(Course).filter(Course.id == data["WebID"])
        course = session.scalars(statement).all()
        course = course[0]

        t.append(course.name)
        t.append(data["question_2"])
        t.append(data["question_3"])
        t.append(data["question_4"])
        t.append(data["question_5"])
        res.append(t)
    data = {'question_1':[], 'question_2':[], 'question_3':[], 'question_4':[], 'question_5':[]}

    for i in range(len(res)):
        for j in range(len(res[i])):
            data["question_{}".format(j+1)].append(res[i][j])
            
    df = pandas.DataFrame(data)
    return df
