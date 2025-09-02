import os

api_key_file = os.getenv("OPENAI_API_KEY_FILE", "/run/secrets/openai_api_key")
with open(api_key_file) as f:
    OPENAI_API_KEY = f.read().strip()

api_app_key_file = os.getenv("API_KEY_FILE", "/run/secrets/api_key")

with open(api_app_key_file) as f:
    API_KEY = f.read().strip()

API_BASE_URL = os.getenv("API_BASE_URL", "http://app:8000")
