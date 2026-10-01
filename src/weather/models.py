from dataclasses import dataclass


@dataclass(frozen=True)
class Weather:
    """Represents the weather data stored for a city."""

    city_name: str
    country: str
    temperature: float
    humidity: int
    desc_en: str
    desc_de: str
