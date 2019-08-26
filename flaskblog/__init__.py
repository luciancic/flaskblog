import os
from flask import Flask
from flaskblog.config.base import BaseConfig
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail



db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()



def create_app(Config: BaseConfig = BaseConfig):
    from flaskblog.main.routes import main
    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts

    app = Flask(__name__)
    app.config.from_object(Config)

    bcrypt.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    login_manager.login_view = 'users.login'
    login_manager.login_message_category = 'info'

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)

    return app
