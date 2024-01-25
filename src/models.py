from flask_sqlalchemy import SQLAlchemy


# A container class `Models` is created for ease of use (the ability to pass all models
# around via one object and access them via dot notation) when working with the ORM
# models. Each ORM model is built using a `db` object that has both a `metadata`
# attribute and a `Model` class. Models are only created for tables that are used in the
# app. Additional models can be created from the remaining tables in the database as
# needed by adding additional inner classes here.
class Models:
    """Container class containing ORM models."""

    def __init__(self, db: SQLAlchemy) -> None:
        """Create ORM models using a database object's metadata attribute.

        Parameters
        ----------
        db : SQLAlchemy
            Flask-SQLAlchemy database object.
        """

        class SeasonRecords(db.Model):
            __table__ = db.metadata.tables["season_records"]

        class TeamsTraditional(db.Model):
            __table__ = db.metadata.tables["teams_traditional"]

        self.SeasonRecords = SeasonRecords
        self.TeamsTraditional = TeamsTraditional
