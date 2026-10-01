import sqlite3
from pathlib import Path

from weather.models import Weather


class WeatherDatabase:
    """Provides SQLite persistence for weather records."""

    def __init__(self, database_path: Path):
        self.database_path = database_path

    def _connect(self) -> sqlite3.Connection:
        """Create a database connection."""

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row

        return connection

    def initialize(self) -> None:
        """Create the weather table if it does not exist."""

        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS weather (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    city_name TEXT NOT NULL UNIQUE,
                    country TEXT NOT NULL,
                    temperature REAL NOT NULL,
                    humidity INTEGER NOT NULL,
                    desc_en TEXT NOT NULL,
                    desc_de TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )

    def get_weather(self, city_name: str) -> Weather | None:
        """Return stored weather for a city."""

        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT
                    city_name,
                    country,
                    temperature,
                    humidity,
                    desc_en,
                    desc_de
                FROM weather
                WHERE city_name = ?
                """,
                (city_name,),
            ).fetchone()

        if row is None:
            return None

        return Weather(
            city_name=row["city_name"],
            country=row["country"],
            temperature=row["temperature"],
            humidity=row["humidity"],
            desc_en=row["desc_en"],
            desc_de=row["desc_de"],
        )

    def insert(self, weather: Weather) -> None:
        """Insert a new weather record."""

        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO weather (
                    city_name,
                    country,
                    temperature,
                    humidity,
                    desc_en,
                    desc_de,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
                """,
                (
                    weather.city_name,
                    weather.country,
                    weather.temperature,
                    weather.humidity,
                    weather.desc_en,
                    weather.desc_de,
                ),
            )

    def update(self, weather: Weather) -> None:
        """Update an existing weather record."""

        with self._connect() as connection:
            connection.execute(
                """
                UPDATE weather
                SET
                    country = ?,
                    temperature = ?,
                    humidity = ?,
                    desc_en = ?,
                    desc_de = ?,
                    updated_at = datetime('now')
                WHERE city_name = ?
                """,
                (
                    weather.country,
                    weather.temperature,
                    weather.humidity,
                    weather.desc_en,
                    weather.desc_de,
                    weather.city_name,
                ),
            )

