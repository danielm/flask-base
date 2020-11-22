#
# By: Daniel Morales <daniminas@gmail.com>
#
# Web: https://github.com/danielm/flask-base
#
# Licence: GPL/MIT
#

from flask import Flask, request, make_response, redirect, render_template, url_for, session, flash
from flask_bootstrap import Bootstrap
import unittest
from functools import wraps

from forms import LoginForm

# Flask instance
app = Flask(__name__, template_folder='./templates', static_folder='./static')
bootstrap = Bootstrap(app)


# Configuration
app.config['SECRET_KEY'] = 'Not_So_Secret' # Needed to use session
app.config['SIMPLE_PASSWORD'] = '1234' # our own stuff, just to implement a simple login


# Simple decorator as only example
def protected_area(func):
  """Checks if user is logged in (keys exists in session)"""
  @wraps(func)
  def wrapper(*args, **kwargs):
    email = session.get('email')
    if not email:
      flash('You must login to access that area', 'warning')
      
      return redirect(url_for('login'))
    
    return func(*args, **kwargs)

  return wrapper


# Homepage (index)
@app.route('/')
def index():
  response = redirect(url_for('hello', name='Joe'))
  
  return response


# Private Area Example
@app.route('/panel')
@protected_area
def panel():
  return render_template('panel.html')


# Example rout with a parameter
@app.route('/hello/<string:name>')
def hello(name):
  cookie_name = 'views_' + name
  views = int(request.cookies.get(cookie_name, 0))
  views += 1

  user_ip = request.remote_addr

  context = {
    'user_ip': user_ip,
    'views': views,
    'name': name,
  }

  response = make_response(render_template('hello.html', **context))
  response.set_cookie(cookie_name, str(views))

  return response


# Login form
@app.route('/login', methods=['GET', 'POST'])
def login():
  login_form = LoginForm()

  if login_form.validate_on_submit():
    email = login_form.email.data
    password = login_form.password.data

    # TODO: Hey dude, add some actual logic here...
    if password == app.config['SIMPLE_PASSWORD']:
      session['email'] = email

      flash('Login successful', 'success')

      return redirect(url_for('panel'))
    else:
      login_form.email.errors.append('Invalid Username/password')

  context = {
    'login_form': login_form,
  }

  return render_template('form.html', **context)


# Log out
@app.route('/logout')
def logout():
  session.pop('email', None)

  flash('Logged out', 'info')

  return redirect(url_for('login'))


# Not Found Error page
@app.errorhandler(404)
def not_found(error):
  return render_template('404.html', error=error)


# Server Error page
@app.errorhandler(500)
def internal_server_error(error):
  return render_template('500.html', error=error)


# Sample command to run Unit tests
@app.cli.command()
def test():
  tests = unittest.TestLoader().discover('tests')
  unittest.TextTestRunner().run(tests)


# Develpment entrypoint
if __name__ == '__main__':
  app.jinja_env.auto_reload = True
  app.config['TEMPLATES_AUTO_RELOAD'] = True
  app.run(debug=True, host='0.0.0.0')