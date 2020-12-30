#
# By: Daniel Morales <daniminas@gmail.com>
#
# Web: https://github.com/danielm/flask-base
#
# Licence: GPL/MIT
#

from flask import request, render_template, session, flash, redirect, url_for
import unittest

from app import create_app
from app.firestore_service import get_users, get_todos, put_todo
from app.forms import TodoForm

from flask_login import login_required, current_user


# Flask instance
app = create_app()


# Homepage (index)
@app.route('/')
def index():
  return render_template('index.html')


# Private Area Example
@app.route('/panel', methods=['GET', 'POST'])
@login_required
def panel():
  user_id = current_user.id

  task_form = TodoForm()

  if task_form.validate_on_submit():
    put_todo(user_id, task_form.description.data)
    flash('New Task created!', 'success')
    return redirect(url_for('panel'))

  context = {
    'todos': get_todos(user_id),
    'task_form': task_form
  }
  return render_template('panel.html', **context)


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