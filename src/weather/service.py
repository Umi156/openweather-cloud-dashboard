import logging

from weather.api_client import OpenWeatherClient
from weather.database import WeatherDatabase


logger = logging.getLogger(__name__)


class WeatherService:
    # """Synchronize OpenWeather data with the local database."""
    """Synchronize OpenWeather data with the database."""

    def __init__(
        self,
        api_client: OpenWeatherClient,
        #database: WeatherDatabase,
        database: WeatherDatabase,
    ):
        self.api_client = api_client
        self.database = database

    def sync_city_weather(self, city: str) -> None:
        """Synchronize weather data for one city."""

        logger.info("Fetching weather for %s", city)

        weather = self.api_client.get_city_weather(city)

        existing = self.database.get_weather(weather.city_name)

        if existing is None:
            self.database.insert(weather)

            logger.info("INSERT %s", weather.city_name)
            return

        if existing == weather:
            logger.info("NO CHANGE %s", weather.city_name)
            return

        self.database.update(weather)

        logger.info("UPDATE %s", weather.city_name)

    def sync_cities(self, cities: tuple[str, ...]) -> None:
        """Synchronize all configured cities."""

        for city in cities:
            try:
                self.sync_city_weather(city)

            except Exception:
                logger.exception("Error syncing %s", city)