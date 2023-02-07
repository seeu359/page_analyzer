import os

from flask import Flask

from page_analyzer.routes import filters, main_routes
from page_analyzer.constants import HTTP_404_NOT_FOUND

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.register_blueprint(main_routes.routes)
app.register_blueprint(filters.filters)
app.register_error_handler(HTTP_404_NOT_FOUND, filters.page_not_found)
