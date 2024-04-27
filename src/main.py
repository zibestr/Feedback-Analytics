from flask import Flask, request, render_template, flash, url_for, send_file, session
from flask_login import LoginManager, UserMixin, login_required, current_user, login_user, logout_user
from werkzeug.utils import secure_filename, redirect
from tools.forms import LoginForm
from tools.password_proccessing import hash_password, check_password
from tools.plot_maker import lesson_stats, pie_plot, keywords_wordcloud
from getDataFromDb import getData
from sqlalchemy import select

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
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = session.query(User).filter(User.nick_name == form.username.data).first()

        if user and check_password(password=form.password.data, key=user.password, salt=user.salt):
            login_user(user, remember=False)
            return redirect(url_for("me", id=user.id))
        
        flash('Пользователь не найден.')
    return render_template("login.html", form=form)


@app.route("/me?<id>", methods=["GET", "POST"])
@login_required
def me(id):
    courses = session.query(Course).all()
    query = select(Feedback).order_by(Feedback.id.desc())
    feedbacks = session.scalars(query).fetchmany(100)

    return render_template("statistics.html", user_type=int(current_user.type), courses=courses)


@app.route("/me?<id>&<course>", methods=["GET", "POST"])
@login_required
def course(id, course: Course):
    return render_template("statistics.html", user_type=int(current_user.type), courses=courses)


@login_manager.user_loader
def load_user(id):
    return session.query(User).get(id)  # session.query(User).filter(User.id == id).first()


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта.")
    return redirect("/")


if __name__ == '__main__':
    os.chdir(os.path.abspath("src/"))
    db_session.global_init(os.path.abspath('db/database.sqlite3'))
    session = db_session.create_session()
    app.run(port=8080, host='0.0.0.0')
