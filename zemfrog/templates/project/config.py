from datetime import timedelta


class Development(object):
    SECRET_KEY = "Your secret key!"
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "JWT secret key!"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)
    DEBUG = True
    EXTENSIONS = [
        "extensions.sqlalchemy",
        "extensions.marshmallow",
        "extensions.migrate",
        "extensions.jwt",
        "extensions.mail",
        "extensions.celery",
    ]
    COMMANDS = [
        "zemfrog.commands.api",
        "zemfrog.commands.blueprint",
        "zemfrog.commands.schema",
        "zemfrog.commands.command",
    ]
    BLUEPRINTS = ["auth"]
    APIS = []
    CREATE_DB = True
    CELERY_RESULT_BACKEND = None
    CELERY_BROKER_URL = None


class Production(Development):
    DEBUG = False
    JWT_COOKIE_SECURE = True


class Testing(Development):
    TESTING = True
