from flask import Flask

from database import get_db_uri
from extensions import cache, db
from models import Models
from routes import create_router

# Initialize and configure the Flask app.
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = get_db_uri()
# Allow for client side caching of static files with max age set to 1 day or 86,400
# seconds.
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 86400

# Initialize the app with the extensions.
db.init_app(app=app)
cache.init_app(app=app)

# Gather table metadata via reflection in order to construct ORM models.
with app.app_context():
    db.reflect()

# Create the ORM models and the router blueprint.
models = Models(db=db)
router = create_router(db=db, models=models)

# Register the router.
app.register_blueprint(blueprint=router)
