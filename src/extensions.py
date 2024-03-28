from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


# Create the model class for Flask-SQLAlchemy.
class Base(DeclarativeBase):
    pass


# Initialize the Flask-SQLAlchemy extension.
db = SQLAlchemy(model_class=Base)
# Initialize the Flask-Caching extension. Default cache timeout is set to 1 day or
# 86,400 seconds.
cache = Cache(config={"CACHE_TYPE": "SimpleCache", "CACHE_DEFAULT_TIMEOUT": 86400})
