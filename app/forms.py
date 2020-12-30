from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, SubmitField, StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, EqualTo

class LoginForm(FlaskForm):
  email = EmailField('E-mail', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  submit = SubmitField('Login')

class SignupForm(FlaskForm):
  email = EmailField('E-mail', validators=[DataRequired()])
  password = PasswordField('Password', validators=[
    DataRequired(),
    EqualTo('confirm', message='Passwords and Confirmation must match')
  ])
  confirm = PasswordField('Repeat password', validators=[DataRequired()])

  submit = SubmitField('Login')

class TodoForm(FlaskForm):
  description = StringField('Description', validators=[DataRequired()])
  submit = SubmitField('Save')