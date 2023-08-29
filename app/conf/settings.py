from decouple import config

SECRET = config('SECRET', cast=str, default='fake-secret')
SQLALCHEMY_DATABASE_URL = config('SQLALCHEMY_DATABASE_URL', cast=str, default='sqlite:///./db.sqlite3')