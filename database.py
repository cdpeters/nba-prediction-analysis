import os
from pathlib import Path


def get_db_uri() -> str:
    """Build database uri from environment variables."""

    # Host, port and database values.
    db = os.environ.get('PGDATABASE')
    host = os.environ.get('PGHOST')
    port = os.environ.get('PGPORT')

    # User credentials.
    user = os.environ.get('PGUSER')
    pwd = os.environ.get('PGPASSWORD')

    # Build database URI.
    db_uri = f"postgresql://{user}:{pwd}@{host}:{port}/{db}"

    return db_uri
