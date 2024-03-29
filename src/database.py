import os
from pathlib import Path

import pandas as pd
from flask_sqlalchemy.extension import SQLAlchemy
from sqlalchemy import and_, between
from sqlalchemy.orm import aliased

from extensions import cache
from models import Models
from utils import convert_frame_to_html


def get_db_uri() -> str:
    """Build database URI from environment variables.

    Returns
    -------
    str
        Database URI string.
    """
    # Host, port and database values.
    db = os.environ.get("PGDATABASE")
    host = os.environ.get("PGHOST")
    port = os.environ.get("PGPORT")

    # User credentials.
    user = os.environ.get("PGUSER")
    pwd = os.environ.get("PGPASSWORD")

    return f"postgresql://{user}:{pwd}@{host}:{port}/{db}"


@cache.cached(key_prefix="get_teams_traditional_table_html")
def get_teams_traditional_table_html(db: SQLAlchemy, models: Models) -> str:
    """Retrieve the teams traditional stat table from the database as html.

    Parameters
    ----------
    db : SQLAlchemy
        Flask-SQLAlchemy database object.
    models : Models
        Container class containing ORM models.

    Returns
    -------
    str
        Teams traditional table as a string of html.
    """
    # Create aliases to reference in the query statement.
    tt = aliased(models.TeamsTraditional)
    sr = aliased(models.SeasonRecords)

    # Build the query statement. In the `join` call below, the `target` argument
    # represents the right table in the join. The left table is inferred from the first
    # table in the `select` call.
    query = (
        db.select(sr, tt)
        .join(
            target=tt,
            onclause=and_(sr.SEASON == tt.SEASON, sr.TEAM == tt.TEAM),
        )
        .where(between(sr.SEASON, 2021, 2022))
    )

    # Execute the query statement.
    teams_traditional = pd.read_sql(sql=query, con=db.engine)
    # Convert "CHAMPION" column to a nullable boolean type in order to set the 2022
    # values for this column to `pd.NA`.
    teams_traditional["CHAMPION"] = teams_traditional["CHAMPION"].astype("boolean")
    teams_traditional.loc[teams_traditional["SEASON"] == 2022, "CHAMPION"] = pd.NA
    # Drop redundant columns from the join.
    teams_traditional = teams_traditional.drop(columns=["SEASON_1", "TEAM_1"])

    return convert_frame_to_html(
        df=teams_traditional,
        border=0,
        classes=[
            "table",
            "table-dark",
            "table-striped",
            "table-borderless",
            "sticky-header",
            "mb-0",
        ],
        index=False,
    )


def get_probability_estimates_table_html(path: Path) -> str:
    """Create the html for the probability estimates table from a csv.

    Parameters
    ----------
    path : Path
        Path to csv file with probability estimates.

    Returns
    -------
    str
        Table html string.
    """
    probability_estimates = pd.read_csv(path)

    return convert_frame_to_html(
        df=probability_estimates,
        border=0,
        classes=[
            "table",
            "table-dark",
            "table-striped",
            "table-borderless",
            "sticky-header",
            "mb-0",
        ],
        index=False,
    )
