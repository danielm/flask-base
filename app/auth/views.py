from flask import redirect, render_template, url_for, flash

from flask import current_app

from flask_login import login_user, login_required, logout_user

from . import auth

from app.firestore_service import get_user
from app.models import UserData, UserModel

from app.forms import LoginForm

# Login form
@auth.route('/login', methods=['GET', 'POST'])
def login():
  login_form = LoginForm()

  if login_form.validate_on_submit():
    email = login_form.email.data
    password = login_form.password.data

    user_doc = get_user(email).to_dict()
    if user_doc is not None:
      if password == user_doc['password']:
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