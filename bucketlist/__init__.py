from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name):
    app = Flask(__name__)
    db.init_app(app)
    login_manager.init_app(app)
    return app

if __name__=='__main__':
    app.run()