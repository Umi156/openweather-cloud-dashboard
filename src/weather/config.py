import os
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(PROJECT_ROOT / ".env")


#API_KEY = os.getenv("OWM_API_KEY")
API_KEY = os.environ["OWM_API_KEY"]

if not API_KEY:
    raise RuntimeError("OWM_API_KEY is not configured.")


BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_API_KEY = os.environ["SUPABASE_API_KEY"]
SUPABASE_DATABASE_URL = os.environ["SUPABASE_DATABASE_URL"]

CITIES = (
    "Berlin",
    "Aachen",
    "Stuttgart",
)

LANGUAGES = (
    "en",
    "de",
)

DATABASE_PATH = PROJECT_ROOT / "data" / "weather.db"

LOG_PATH = PROJECT_ROOT / "logs" / "app.log"