import os
from flask import Flask
from sqlalchemy import *
from sqlalchemy import NullPool


def create_app():
    tmpl_dir = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'templates')
    app = Flask(__name__, template_folder=tmpl_dir)

    DATABASE_USERNAME = "rl3176"
    DATABASE_PASSWRD = "2727"
    DATABASE_HOST = "34.28.53.86"
    DATABASEURI = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWRD}@{DATABASE_HOST}/project1"

    engine = create_engine(DATABASEURI)

    @app.before_request
    def before_request():
        try:
            conn = engine.connect()
        except:
            print("uh oh, problem connecting to database")
            import traceback
            traceback.print_exc()
            conn = None

    @app.teardown_request
    def teardown_request(exception):
        try:
            conn.close()
        except Exception as e:
            pass

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app
