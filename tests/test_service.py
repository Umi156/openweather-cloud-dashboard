from pathlib import Path

from weather.database import WeatherDatabase
from weather.models import Weather
from weather.service import WeatherService


class FakeApiClient:
    """Fake API client used for testing without calling OpenWeather."""

    def __init__(self, weather: Weather):
        self.weather = weather

    def get_city_weather(self, city: str) -> Weather:
        return self.weather


def create_weather(
    temperature: float = 15.5,
) -> Weather:
    return Weather(
        city_name="Berlin",
        country="DE",
        temperature=temperature,
        humidity=70,
        desc_en="clear sky",
        desc_de="klarer Himmel",
    )


def create_service(
    tmp_path: Path,
    weather: Weather,
) -> tuple[WeatherService, WeatherDatabase]:
    database = WeatherDatabase(tmp_path / "test.db")
    database.initialize()

    api_client = FakeApiClient(weather)

    service = WeatherService(
        api_client=api_client,
        database=database,
    )

    return service, database


def test_insert_when_city_does_not_exist(tmp_path: Path):
    weather = create_weather()

    service, database = create_service(
        tmp_path,
        weather,
    )

    service.sync_city_weather("Berlin")

    stored = database.get_weather("Berlin")

    assert stored == weather


def test_no_update_when_weather_is_unchanged(tmp_path: Path):
    weather = create_weather()

    service, database = create_service(
        tmp_path,
        weather,
    )

    database.insert(weather)

    service.sync_city_weather("Berlin")

    stored = database.get_weather("Berlin")

    assert stored == weather


def test_update_when_weather_has_changed(tmp_path: Path):
    old_weather = create_weather(temperature=15.5)

    new_weather = create_weather(temperature=18.2)

    service, database = create_service(
        tmp_path,
        new_weather,
    )

    database.insert(old_weather)

    service.sync_city_weather("Berlin")

    stored = database.get_weather("Berlin")

    assert stored == new_weather