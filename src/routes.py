from pathlib import Path

from flask import Blueprint, render_template
from flask.wrappers import Response
from flask_sqlalchemy.extension import SQLAlchemy

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
    def index() -> str:
        """Render landing page with the overview of the project."""
        team_trad_table_html = get_teams_traditional_table_html(db=db, models=models)
        return render_template("index.html", team_trad_table_html=team_trad_table_html)

    @router.route("/game-evolution")
    def game_evolution() -> str:
        """Render page containing analysis of the modern game."""
        return render_template("game_evolution.html")

    @router.route("/defense-offense")
    def defense_offense() -> str:
        """Render overview of offensive/defensive stats for current teams."""
        return render_template("defense_offense.html")

    @router.route("/comparison")
    def comparison() -> str:
        """Render page with current playoff teams vs. past champions comparisons."""
        return render_template("comparison.html")

    @router.route("/prediction")
    def prediction() -> str:
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
    def people() -> str:
        """Render developer team information."""
        return render_template("people.html")

    @router.route("/glossary")
    def glossary() -> str:
        """Render glossary for stat type abbreviations."""
        return render_template("glossary.html")

    @router.after_request
    def add_cache_control(response: Response) -> Response:
        """Add cache control header to response object to allow client side caching.

        Parameters
        ----------
        response : Response
            The response to the incoming request.

        Returns
        -------
        Response
            Modified response with cache control header set.
        """
        # Set the cache control header with the max-age set to 1 day or 86,400 seconds.
        response.headers["Cache-Control"] = "public, max-age=86400"
        return response

    return router
