from flask import redirect, render_template, url_for, flash, session

from flask import current_app

from . import auth

from app.forms import LoginForm

# Login form
@auth.route('/login', methods=['GET', 'POST'])
def login():
  login_form = LoginForm()

  if login_form.validate_on_submit():
    email = login_form.email.data
    password = login_form.password.data

    # TODO: Hey dude, add some actual logic here...
    if password == current_app.config['SIMPLE_PASSWORD']:
      session['email'] = email

      flash('Login successful', 'success')

      return redirect(url_for('panel'))
    else:
      login_form.email.errors.append('Invalid Username/password')

  context = {
    'login_form': login_form,
  }

  return render_template('login.html', **context)


# Log out
@auth.route('/logout')
def logout():
  session.pop('email', None)

  flash('Logged out', 'info')

  return redirect(url_for('auth.login'))