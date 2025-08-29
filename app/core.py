import os
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

class Settings:
    YF_PERIOD = os.getenv("YF_PERIOD", "2y")
    YF_INTERVAL = os.getenv("YF_INTERVAL", "1d")
    CACHE_MINUTES = int(os.getenv("CACHE_MINUTES", 30))
    DB_URL = os.getenv("DB_URL", "sqlite:///./stocksense.db")

@lru_cache
def get_settings():
    return Settings()
