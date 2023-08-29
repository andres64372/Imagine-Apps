from decouple import config

SECRET = config('SECRET', cast=str)
SQLALCHEMY_DATABASE_URL = config('SQLALCHEMY_DATABASE_URL', cast=str, default='sqlite:///./db.sqlite3')