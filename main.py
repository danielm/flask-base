#
# By: Daniel Morales <daniminas@gmail.com>
#
# Web: https://github.com/danielm/flask-base
#
# Licence: GPL/MIT
#

from flask import render_template
import unittest
import babel

from app import create_app


# Flask instance
app = create_app()


# Homepage (index)
@app.route('/')
def index():
  return render_template('index.html')

# Not Found Error page
@app.errorhandler(404)
def not_found(error):
  return render_template('404.html', error=error)


# Server Error page
@app.errorhandler(500)
def internal_server_error(error):
  return render_template('500.html', error=error)


#Simple jinja2 filter
@app.template_filter()
def format_datetime(value, format='medium'):
  if format == 'full':
    format="EEEE, d. MMMM y 'at' HH:mm"
  elif format == 'medium':
    format="EE dd.MM.y HH:mm"
  return babel.dates.format_datetime(value, format)


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