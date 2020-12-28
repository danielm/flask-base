#
# By: Daniel Morales <daniminas@gmail.com>
#
# Web: https://github.com/danielm/flask-base
#
# Licence: GPL/MIT
#

from flask import request, make_response, redirect, render_template, url_for, session, flash
import unittest

from app import create_app
from app.auth import protected_area

# Flask instance
app = create_app()


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


# Not Found Error page
@app.errorhandler(404)
def not_found(error):
  return render_template('404.html', error=error)


# Server Error page
@app.errorhandler(500)
def internal_server_error(error):
  return render_template('500.html', error=error)


# Sample command to run Unit tests
@app.cli.command(name='test', help='Some basic')
def test():
  tests = unittest.TestLoader().discover('tests')
  unittest.TextTestRunner().run(tests)


# Develpment entrypoint
if __name__ == '__main__':
  app.jinja_env.auto_reload = True
  app.config['TEMPLATES_AUTO_RELOAD'] = True
  app.run(debug=True, host='0.0.0.0')