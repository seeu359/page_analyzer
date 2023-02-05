import os

from flask import Flask

from page_analyzer.routes import main_routes, filters


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.register_blueprint(main_routes.routes)
app.register_error_handler(404, filters.page_not_found)
