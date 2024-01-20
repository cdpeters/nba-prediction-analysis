from flask import Blueprint, render_template
from flask_sqlalchemy import SQLAlchemy

from database import get_teams_traditional_table_html
from models import Models


def create_router(db: SQLAlchemy, models: Models) -> Blueprint:
    """Create a Flask router blueprint.

    The blueprint contains all page routes for the app with calls to `render_template`
    providing any data required for the rendering of the html template. The blueprint is
    registered with the app in app.py.

    Parameters
    ----------
    db : SQLAlchemy
        Flask-SQLAlchemy database object.
    models : Models
        Container class containing ORM models.

    Returns
    -------
    Blueprint
        Flask blueprint representing the router for the app.
    """
    router = Blueprint("router", __name__)

    @router.route("/")
    def index():
        """Render landing page with the overview of the project."""
        return render_template("index.html")

    @router.route("/game_evolution")
    def game_evolution():
        """Render page containing analysis of the modern game."""
        table_html = get_teams_traditional_table_html(db, models)
        return render_template("game_evolution.html", table_html=table_html)

    @router.route("/defense_offense")
    def defense_offense():
        """Render overview of offensive/defensive stats for current teams."""
        return render_template("defense_offense.html")

    @router.route("/comparison")
    def comparison():
        """Render page with current playoff teams vs. past champions comparisons."""
        return render_template("comparison.html")

    @router.route("/prediction")
    def prediction():
        """Render page with machine learning analysis and final champion prediction."""
        return render_template("prediction.html")

    @router.route("/people")
    def people():
        """Render developer team information."""
        return render_template("people.html")

    @router.route("/glossary")
    def glossary():
        """Render glossary for stat type abbreviations."""
        return render_template("glossary.html")

    return router
