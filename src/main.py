from flask import Flask, request, render_template, flash, url_for, send_file, session
from werkzeug.utils import secure_filename, redirect
from tools.forms import LoginForm, RegForm
from tools.password_proccessing import hash_password, check_password

from db_models.__all_models import *
from db_models import db_session
import os

app = Flask(__name__)
app.secret_key = '379cc9d0797b7d3a445eae49288768c6'
app.config['SECRET_KEY'] = '379cc9d0797b7d3a445eae49288768c6'


if __name__ == '__main__':
    os.chdir(os.path.abspath("src/"))
    db_session.global_init(os.path.abspath('db/database.sqlite3'))
    session = db_session.create_session()
    app.run(port=8080, host='127.0.0.1')
