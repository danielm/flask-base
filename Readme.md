This is a base monolithic application project for flask shenanigans adn testing. This is a WIP not so serious.... so why are you?

virtualenv venv
source venv/bin/activate
pip install -r requirements.txt 

export FLASK_APP=main.py
export FLASK_DEBUG=1
export FLASK_ENV=development

flask run
flask test

Vagrant
flask run -h 0.0.0.0