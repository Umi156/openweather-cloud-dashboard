from fastapi import FastAPI, HTTPException

from weather.api_client import OpenWeatherClient
from weather.config import API_KEY, CITIES
from weather.service import WeatherService
from weather.supabase_client import get_supabase_client
from weather.supabase_database import SupabaseWeatherDatabase


app = FastAPI(
    title="OpenWeather Supabase API",
    version="1.0.0",
)

supabase = get_supabase_client()
database = SupabaseWeatherDatabase(client=supabase)

api_client = OpenWeatherClient(API_KEY)

service = WeatherService(
    api_client=api_client,
    database=database,
)

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/weather")
def get_all_weather() -> list[dict]:
    weather_records = database.get_all_weather()

    return [
        {
            "city_name": weather.city_name,
            "country": weather.country,
            "temperature": weather.temperature,
            "humidity": weather.humidity,
            "desc_en": weather.desc_en,
            "desc_de": weather.desc_de,
        }
        for weather in weather_records
    ]


@app.get("/weather/{city}")
def get_city_weather(city: str) -> dict:
    weather = database.get_weather(city)

    if weather is None:
        raise HTTPException(
            status_code=404,
            detail=f"Weather for {city} not found",
        )

    return {
        "city_name": weather.city_name,
        "country": weather.country,
        "temperature": weather.temperature,
        "humidity": weather.humidity,
        "desc_en": weather.desc_en,
        "desc_de": weather.desc_de,
    }


@app.post("/weather/sync")
def sync_all_weather() -> dict:
    for city in CITIES:
        service.sync_city_weather(city)

    return {
        "status": "synchronized",
        "cities": list(CITIES),
    }


@app.post("/weather/{city}/sync")
def sync_city_weather(city: str) -> dict:
    service.sync_city_weather(city)

    weather = database.get_weather(city)

    if weather is None:
        raise HTTPException(
            status_code=404,
            detail=f"Weather for {city} not found",
        )

    return {
        "status": "synchronized",
        "city_name": weather.city_name,
        "temperature": weather.temperature,
        "humidity": weather.humidity,
        "description": weather.desc_en,
    }