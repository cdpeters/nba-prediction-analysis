import tomllib
from pathlib import Path


def get_db_uri() -> str:
    """Build database uri from secrets file."""
    secrets_path = Path.cwd() / "secrets.toml"

    with open(secrets_path, "rb") as f:
        secrets = tomllib.load(f)

    # Host, port and database values.
    host = secrets["DATABASE"]["HOST"]
    port = secrets["DATABASE"]["PORT"]
    db = secrets["DATABASE"]["DB"]

    # User credentials.
    user = secrets["USER"]["USERNAME"]
    pwd = secrets["USER"]["PASSWORD"]

    # Build database URI.
    db_uri = f"postgresql://{user}:{pwd}@{host}:{port}/{db}"

    return db_uri
