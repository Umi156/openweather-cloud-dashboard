from datetime import datetime, timezone

from supabase import Client

from weather.models import Weather


class SupabaseWeatherDatabase:
    """Provides Supabase Data API persistence for weather records."""

    def __init__(self, client: Client):
        self.client = client

    def get_weather(
        self,
        city_name: str,
    ) -> Weather | None:
        """Return stored weather for a city."""

        response = (
            self.client.table("weather")
            .select(
                "city_name,"
                "country,"
                "temperature,"
                "humidity,"
                "desc_en,"
                "desc_de"
            )
            .eq("city_name", city_name)
            .limit(1)
            .execute()
        )
        
        if not response.data:
            return None
        
        row = response.data[0]

        return Weather(
            city_name=row["city_name"],
            country=row["country"],
            temperature=row["temperature"],
            humidity=row["humidity"],
            desc_en=row["desc_en"],
            desc_de=row["desc_de"],
        )

    def insert(
        self,
        weather: Weather,
    ) -> None:
        """Insert a new weather record."""

        (
            self.client.table("weather")
            .insert(
                {
                    "city_name": weather.city_name,
                    "country": weather.country,
                    "temperature": weather.temperature,
                    "humidity": weather.humidity,
                    "desc_en": weather.desc_en,
                    "desc_de": weather.desc_de,
                    "updated_at": datetime.now(
                        timezone.utc
                    ).isoformat(),
                }
            )
            .execute()
        )

    def update(
        self,
        weather: Weather,
    ) -> None:
        """Update an existing weather record."""

        (
            self.client.table("weather")
            .update(
                {
                    "country": weather.country,
                    "temperature": weather.temperature,
                    "humidity": weather.humidity,
                    "desc_en": weather.desc_en,
                    "desc_de": weather.desc_de,
                    "updated_at": datetime.now(
                        timezone.utc
                    ).isoformat(),
                }
            )
            .eq("city_name", weather.city_name)
            .execute()
        )

    def get_all_weather(self) -> list[Weather]:
        """Return all stored weather records."""

        response = (
            self.client.table("weather")
            .select(
                "city_name,"
                "country,"
                "temperature,"
                "humidity,"
                "desc_en,"
                "desc_de"
            )
            .order("city_name")
            .execute()
        )

        return [
            Weather(
                city_name=row["city_name"],
                country=row["country"],
                temperature=row["temperature"],
                humidity=row["humidity"],
                desc_en=row["desc_en"],
                desc_de=row["desc_de"],
            )
            for row in response.data
        ]