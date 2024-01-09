import pandas as pd
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

from database import get_db_uri


# Configure App and SQLAlchemy `db` Object ---------------------------------------------
class Base(DeclarativeBase):
    pass


# Create the `db` object based on a DeclarativeBase model.
db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
# Configure the database URI on the `app` object.
app.config["SQLALCHEMY_DATABASE_URI"] = get_db_uri()


# Initialize App and ORM Mapped Classes ------------------------------------------------
with app.app_context():
    # Initialize the app with the extension.
    db.init_app(app)
    # Gather metadata by reflecting the database.
    db.reflect()


# Build the ORM classes using the metadata collected by `db.reflect()`. The
# `playoff_teams` table is left out due to its lack of primary key, see
# `playoff_teams_long` for the same information.
class Teams(db.Model):
    __table__ = db.metadata.tables["teams"]


class Seasons(db.Model):
    __table__ = db.metadata.tables["seasons"]


class SeasonRecords(db.Model):
    __table__ = db.metadata.tables["season_records"]


class PlayoffRecords(db.Model):
    __table__ = db.metadata.tables["playoff_records"]


class TeamsTraditional(db.Model):
    __table__ = db.metadata.tables["teams_traditional"]


class TeamsAdvanced(db.Model):
    __table__ = db.metadata.tables["teams_advanced"]


class TeamsMisc(db.Model):
    __table__ = db.metadata.tables["teams_misc"]


class TeamsClutch(db.Model):
    __table__ = db.metadata.tables["teams_clutch"]


class PlayoffsTraditional(db.Model):
    __table__ = db.metadata.tables["playoffs_traditional"]


class PlayoffsAdvanced(db.Model):
    __table__ = db.metadata.tables["playoffs_advanced"]


class PlayoffsMisc(db.Model):
    __table__ = db.metadata.tables["playoffs_misc"]


class PlayoffsClutch(db.Model):
    __table__ = db.metadata.tables["playoffs_clutch"]


class PlayoffTeamsLong(db.Model):
    __table__ = db.metadata.tables["playoff_teams_long"]


class Champions(db.Model):
    __table__ = db.metadata.tables["champions"]


# App Routes ---------------------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/game_evolution")
def game_evolution():
    with app.app_context():
        query = (
            db.select(SeasonRecords, TeamsTraditional)
            .join(
                TeamsTraditional,
                (SeasonRecords.SEASON == TeamsTraditional.SEASON)
                & (SeasonRecords.TEAM == TeamsTraditional.TEAM),
            )
            .where(SeasonRecords.SEASON <= 2022)
        )
        teams_traditional = pd.read_sql(sql=query, con=db.engine)
        teams_traditional = teams_traditional.drop(columns=["SEASON_1", "TEAM_1"])

    table_html = teams_traditional.to_html(
        justify="left",
        border=0,
        classes=["table", "table-dark", "table-striped"],
        index=False,
    )
    return render_template("game_evolution.html", table_html=table_html)


@app.route("/defense_offense")
def defense_offense():
    return render_template("defense_offense.html")


@app.route("/comparison")
def comparison():
    return render_template("comparison.html")


@app.route("/prediction")
def prediction():
    return render_template("prediction.html")


@app.route("/people")
def people():
    return render_template("people.html")


@app.route("/glossary")
def glossary():
    return render_template("glossary.html")


if __name__ == "__main__":
    app.run(debug=True)
