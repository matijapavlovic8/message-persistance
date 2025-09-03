import os
from time import sleep

def get_secret(name: str, default: str | None = None) -> str | None:
    """
    Retrieve a secret value from a file or environment variable.

    The function first looks for an environment variable pointing to a secret file,
    named `{name}_FILE`. If the file exists, it reads and returns the content.
    If the file is not found immediately, it retries up to 5 seconds.
    If no file is found, it falls back to an environment variable named `{name}`,
    or returns the provided `default` value.

    Args:
        name (str): The base name of the secret (e.g., "OPENAI_API_KEY").
        default (str | None, optional): A default value to return if the secret is not found. Defaults to None.

    Returns:
        str | None: The secret value if found, otherwise the default.
    """
    file_path = os.getenv(f"{name}_FILE")
    if file_path:
        for _ in range(5):
            if os.path.exists(file_path):
                with open(file_path) as f:
                    return f.read().strip()
            sleep(1)
    return os.getenv(name, default)

DB_USER = "postgres"
DB_NAME = "messages_db"
DB_HOST = "db"
DB_PASSWORD = get_secret("DB_PASSWORD")
API_KEY = get_secret("API_KEY")

if DB_PASSWORD is None:
    raise ValueError("DB_PASSWORD is not set, check Docker secret mounting!")

class Settings:
    database_url: str = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
    api_key: str = API_KEY

settings = Settings()
