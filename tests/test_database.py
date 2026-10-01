from pathlib import Path

from weather.database import WeatherDatabase
from weather.models import Weather


def test_insert_and_get_weather(tmp_path: Path):
    database = WeatherDatabase(
        tmp_path / "test.db"
    )

    database.initialize()

    weather = Weather(
        city_name="Berlin",
        country="DE",
        temperature=15.5,
        humidity=70,
        desc_en="clear sky",
        desc_de="klarer Himmel",
    )

    database.insert(weather)

    result = database.get_weather("Berlin")

    assert result == weather
