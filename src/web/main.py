from flask import Flask
from models import db_session

app = Flask(__name__)
# app.secret_key = '379cc9d0797b7d3a445eae49288768c6'
# app.config['SECRET_KEY'] = '379cc9d0797b7d3a445eae49288768c6'


if __name__ == '__main__':
    db_session.global_init('db/database.sqlite')
    session = db_session.create_session()
    app.run(port=8080, host='127.0.0.1')