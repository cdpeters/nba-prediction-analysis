import os

import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from sqlalchemy.orm import aliased

from models import Models


def get_db_uri() -> str:
    """Build database uri from environment variables.

    Returns
    -------
    str
        Database uri string.
    """
    # Host, port and database values.
    db = os.environ.get("PGDATABASE")
    host = os.environ.get("PGHOST")
    port = os.environ.get("PGPORT")

    # User credentials.
    user = os.environ.get("PGUSER")
    pwd = os.environ.get("PGPASSWORD")

    # Build database URI.
    db_uri = f"postgresql://{user}:{pwd}@{host}:{port}/{db}"

    return db_uri


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

    # In the `join` call below, the `target` argument represents the right table in the
    # join. The left table is inferred from the first table in the `select` call.
    query = (
        db.select(sr, tt)
        .join(
            target=tt,
            onclause=and_(sr.SEASON == tt.SEASON, sr.TEAM == tt.TEAM),
        )
        .where(sr.SEASON <= 2022)
    )

    # Execute the query statement using pandas `read_sql`.
    teams_traditional = pd.read_sql(sql=query, con=db.engine)
    # Drop redundant columns from the join.
    teams_traditional = teams_traditional.drop(columns=["SEASON_1", "TEAM_1"])

    return teams_traditional.to_html(
        justify="left",
        border=0,
        classes=["table", "table-dark", "table-striped"],
        index=False,
    )
