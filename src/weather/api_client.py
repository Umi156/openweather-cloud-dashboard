import requests

from weather.config import BASE_URL
from weather.models import Weather


class OpenWeatherClient:
    """Client for retrieving weather data from OpenWeather."""

    def __init__(self, api_key: str):
        self.api_key = api_key

    def _request_weather(
        self,
        city: str,
        language: str,
    ) -> dict:
        """Request weather data for a city and language."""

        params = {
            "q": f"{city},DE",
            "appid": self.api_key,
            "units": "metric",
            "lang": language,
        }

        response = requests.get(
            BASE_URL,
            params=params,
            timeout=10,
        )

        response.raise_for_status()

        return response.json()

    def get_city_weather(self, city: str) -> Weather:
        """Retrieve English and German weather descriptions."""

        data_en = self._request_weather(city, "en")
        data_de = self._request_weather(city, "de")

        return Weather(
            city_name=data_en["name"],
            country=data_en["sys"]["country"],
            temperature=data_en["main"]["temp"],
            humidity=data_en["main"]["humidity"],
            desc_en=data_en["weather"][0]["description"],
            desc_de=data_de["weather"][0]["description"],
        )