from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import app_config
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])

    db.init_app(app)
    migrate = Migrate(app, db)

    # register the apivi blueprint.
    from .api_v1 import apiv1 as api_blueprint
    app.register_blueprint(api_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    from bucketlist import models

    return app

if __name__ == '__main__':
    app.run()
