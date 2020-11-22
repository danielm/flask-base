from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
  email = EmailField('E-mail', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  submit = SubmitField('Login')