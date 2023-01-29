import os

from flask import Flask

from page_analyzer.routes import routes

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.register_blueprint(routes)
