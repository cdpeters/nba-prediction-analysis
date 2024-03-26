from pathlib import Path

from flask import Blueprint, render_template
from flask_sqlalchemy import SQLAlchemy

from database import (
    get_probability_estimates_table_html,
    get_teams_traditional_table_html,
)
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
        team_trad_table_html = get_teams_traditional_table_html(db=db, models=models)
        return render_template("index.html", team_trad_table_html=team_trad_table_html)

    @router.route("/game-evolution")
    def game_evolution():
        """Render page containing analysis of the modern game."""
        return render_template("game_evolution.html")

    @router.route("/defense-offense")
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
        DATA_DIR = Path.cwd() / "data"
        proba_est_table_html = get_probability_estimates_table_html(
            path=DATA_DIR / "probability_estimates.csv"
        )
        return render_template(
            "prediction.html",
            proba_est_table_html=proba_est_table_html,
        )

    @router.route("/people")
    def people():
        """Render developer team information."""
        return render_template("people.html")

    @router.route("/glossary")
    def glossary():
        """Render glossary for stat type abbreviations."""
        return render_template("glossary.html")

    return router
