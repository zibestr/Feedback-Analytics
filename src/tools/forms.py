from wtforms import Form, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign in')
