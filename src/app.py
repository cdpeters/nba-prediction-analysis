from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

from database import get_db_uri
from models import Models
from routes import create_router

# Initialize and configure the Flask app.
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = get_db_uri()


# Initialize Flask-SQLAlchemy extension.
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

# Configure the extension (connect the extension to the Flask app).
db.init_app(app)

# Gather table metadata via reflection in order to construct ORM models.
with app.app_context():
    db.reflect()

# Create the ORM models and the router blueprint.
models = Models(db)
router = create_router(db, models)

# Register the router.
app.register_blueprint(router)
