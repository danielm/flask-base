from flask import redirect, render_template, url_for, flash

from flask import current_app

from flask_login import login_user, login_required, logout_user

from werkzeug.security import generate_password_hash, check_password_hash

from . import auth

from app.firestore_service import get_user, user_put
from app.models import UserData, UserModel

from app.forms import LoginForm, SignupForm

# Login form
@auth.route('/login', methods=['GET', 'POST'])
def login():
  login_form = LoginForm()

  if login_form.validate_on_submit():
    email = login_form.email.data
    password = login_form.password.data

    user_doc = get_user(email).to_dict()
    if user_doc is not None:
      if check_password_hash(user_doc['password'], password):
        user_data = UserData(email, password)
        user = UserModel(user_data)

        login_user(user)

        flash('Login successful', 'success')

        return redirect(url_for('panel'))
      else:
        login_form.email.errors.append('Invalid Username/password')
    else:
      login_form.email.errors.append('User not found')

  context = {
    'login_form': login_form,
  }

  return render_template('login.html', **context)


# Log out
@auth.route('/logout')
@login_required
def logout():
  logout_user()

  flash('Logged out', 'info')

  return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
  signup_form = SignupForm()

  if signup_form.validate_on_submit():
    email = signup_form.email.data
    password = signup_form.password.data

    user_doc = get_user(email).to_dict()
    if user_doc is None:
      password_hash = generate_password_hash(password)
      user_data = UserData(email, password_hash)

      user_put(user_data)

      user = UserModel(user_data)
      login_user(user)

      flash('Welcome to our app', 'success')

      return redirect(url_for('panel'))
    else:
      signup_form.email.errors.append('User already exists')

  context = {
    'signup_form': signup_form,
  }

  return render_template('signup.html', **context)