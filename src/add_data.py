from db_models.users import User
from db_models.courses import Course
from db_models.feedbacks import Feedback
from db_models import db_session
from tools.password_proccessing import hash_password, check_password
import os
import csv
from pathlib import Path


def add_user(nick_name, user_type, password):
    key, salt = hash_password(password=password)
    user = User(nick_name=nick_name,
                type=user_type,
                password=key,
                salt=salt)
    session.add(user)
    session.commit()


def add_course(name):
    course = Course(name=name)
    session.add(course)
    session.commit()


def add_feedback(questions: dict):
    questions["WebID"] = session.query(Course).filter(Course.name == questions["question_1"]).first().id
    del questions["question_1"]
    del questions["timestamp"]
    del questions["is_relevant"]
    del questions["object"]
    del questions["is_positive"]

    serialized = str(questions)

    feedback = Feedback(answers=serialized)

    session.add(feedback)
    session.commit()
    
    
if __name__ == "__main__":
    os.chdir(os.path.abspath("src/"))
    db_session.global_init(os.path.abspath('db/database.sqlite3'))
    session = db_session.create_session()

    users = [["boss", 0, "boss"],
             ["admin", 0, "admin"],
             ["a", 0, "a"]]
    for user in users:
        add_user(*user)
    
    os.chdir(os.path.abspath("../"))
    with open('data/train_data.csv', newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            if not session.query(Course).filter(Course.name == row["question_1"]).first():
                add_course(name=row["question_1"])
            if i % 5 == 0:
                add_feedback(row)
    