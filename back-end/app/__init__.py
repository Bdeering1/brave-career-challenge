from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('config.py')

print(app.config['TEST_KEY'])

from app import routes
