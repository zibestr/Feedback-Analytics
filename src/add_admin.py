from db_models.users import User
from db_models.courses import Course
from db_models import db_session
from tools.password_proccessing import hash_password, check_password
import os


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
    
    
if __name__ == "__main__":
    os.chdir(os.path.abspath("src/"))
    db_session.global_init(os.path.abspath('db/database.sqlite3'))
    session = db_session.create_session()

    users = [["boss", 0, "boss"],
             ["admin", 0, "admin"],
             ["a", 0, "a"]]
    for user in users:
        add_user(*user)

    courses = ["Программирование на языке Python",
               "Разработка децентрализованных систем",
               "Будущее IT. Тренды"]
    for course in courses:
        add_course(course)
    