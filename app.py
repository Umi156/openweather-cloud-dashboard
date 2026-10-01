import logging

from weather.api_client import OpenWeatherClient
from weather.supabase_client import get_supabase_client
# from weather.config import API_KEY, CITIES, DATABASE_PATH, LOG_PATH
from weather.config import API_KEY, CITIES, LOG_PATH, SUPABASE_DATABASE_URL
#from weather.database import WeatherDatabase
from weather.supabase_database import SupabaseWeatherDatabase
from weather.logger import configure_logging
from weather.service import WeatherService


logger = logging.getLogger(__name__)


def main() -> None:
    """Run the weather synchronization application."""

    configure_logging(LOG_PATH)

    logger.info("Starting weather synchronization")

    # database = WeatherDatabase(DATABASE_PATH)
    # database.initialize()

    # Create Supabase connection
    supabase = get_supabase_client()

    # Create database repository using Supabase
    database = SupabaseWeatherDatabase(
    client=supabase,)

    # Create OpenWeatherMap client
    api_client = OpenWeatherClient(API_KEY)

    service = WeatherService(
        api_client=api_client,
        database=database,
    )

    service.sync_cities(CITIES)

    logger.info("Weather synchronization finished")


if __name__ == "__main__":
    main()
