import tomllib
from pathlib import Path


def get_db_uri():
    secrets_path = Path("secrets.toml")

    with open(secrets_path, "rb") as f:
        secrets = tomllib.load(f)

    # database and root user credentials
    host = secrets["DATABASE"]["HOST"]
    port = secrets["DATABASE"]["PORT"]
    db = secrets["DATABASE"]["DB"]

    # user credentials
    user = secrets["USER"]["USERNAME"]
    pwd = secrets["USER"]["PASSWORD"]

    # user db url
    db_url = f"postgresql://{user}:{pwd}@{host}:{port}/{db}"

    return db_url
