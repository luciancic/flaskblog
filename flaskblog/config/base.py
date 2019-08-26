from flaskblog.config.config_private import MailConfig

class BaseConfig(MailConfig):
    SECRET_KEY = 'in1324k8dxg93ui2nr1o'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True


class TestConfig(BaseConfig):
    TESTING = True
    SECRET_KEY = 'wejn1rkjn9v0df21fe5dfhh'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    