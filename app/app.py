from flask import Flask, g

from flask_login import LoginManager, user_loaded_from_header
from flask_swagger_ui import get_swaggerui_blueprint
from flask.sessions import SecureCookieSessionInterface
from db import db
from todo import routes
#from config import config

from user_api import user_api_blueprint
from todo import todo_api_blueprint
app = Flask(__name__)
login_manager = LoginManager(app)
login_manager.init_app(app)

app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    auth_plugin='mysql_native_password',
    SQLALCHEMY_TRACK_MODIFICATIONS='True',
))
"""
models.init_app(app)
models.create_tables(app)"""
app.register_blueprint(todo_api_blueprint)

app.register_blueprint(user_api_blueprint)

SWAGGER_URL = '/api/docs'
API_URL = '/api/user/docs.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(db.User).filter_by(id=user_id).first()


@login_manager.request_loader
def load_user_from_request(request):

    # try to login using Basic Auth
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        user = models.User.query.filter_by(api_key=api_key).first()
        if user:
            return user

    return None


class CustomSessionInterface(SecureCookieSessionInterface):
    """Prevent creating session from API requests."""

    def save_session(self, *args, **kwargs):
        if g.get('login_via_header'):
            return
        return super(CustomSessionInterface, self).save_session(*args, **kwargs)


app.session_interface = CustomSessionInterface()


@user_loaded_from_header.connect
def user_loaded_from_header(self, user=None):
    g.login_via_header = True

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
