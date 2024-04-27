from flask import Flask, request, render_template, flash, url_for, send_file, session
from flask_login import LoginManager, UserMixin, login_required, current_user, login_user, logout_user
from werkzeug.utils import secure_filename, redirect
from tools.forms import LoginForm
from tools.password_proccessing import hash_password, check_password

from db_models.courses import Course
from db_models.feedbacks import Feedback
from db_models.students import Student
from db_models.users import User
from db_models import db_session
import os

app = Flask(__name__)
login_manager = LoginManager(app)
app.secret_key = 'whgt9jasqzctj24yg79ve5za6jnwfzqg'
app.config['SECRET_KEY'] = 'whgt9jasqzctj24yg79ve5za6jnwfzqg'


@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def homepage():
    # TODO Здесь описание проекта в шаблоне и форма login
    return render_template("login.html")


@app.route("/me?<id>", methods=["GET", "POST"])
@login_required
def me(id):
    # TODO сюда перенаправляется пользователь после логина, здесь статистика
    return render_template("index.html")


@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect("/")


if __name__ == '__main__':
    os.chdir(os.path.abspath("src/"))
    db_session.global_init(os.path.abspath('db/database.sqlite3'))
    session = db_session.create_session()
    app.run(port=8080, host='127.0.0.1')
