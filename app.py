#
# By: Daniel Morales <daniminas@gmail.com>
#
# Web: https://github.com/danielm/flask-base
#
# Licence: GPL/MIT
#

from flask import Flask, request, make_response, redirect, render_template, url_for

app = Flask(__name__, template_folder='./templates', static_folder='./static')


# Homepage (index)
@app.route('/')
def index():
  response = make_response(redirect(url_for('hello', name='Joe')))
  
  return response


# Example rout with a parameter
@app.route('/hello/<string:name>')
def hello(name):
  views = int(request.cookies.get('views', 0))
  views += 1

  user_ip = request.remote_addr

  context = {
    'user_ip': user_ip,
    'views': views,
    'name': name,
  }

  response = make_response(render_template('hello.html', **context))
  response.set_cookie('views', str(views))

  return response


# Not Found Error page
@app.errorhandler(404)
def not_found(error):
  return render_template('404.html', error=error)


# Server Error page
@app.errorhandler(500)
def internal_server_error(error):
  return render_template('500.html', error=error)

# Develpment entrypoint
if __name__ == '__main__':
  app.jinja_env.auto_reload = True
  app.config['TEMPLATES_AUTO_RELOAD'] = True
  app.run(debug=True, host='0.0.0.0')