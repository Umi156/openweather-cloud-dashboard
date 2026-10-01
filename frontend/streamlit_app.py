import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="Weather Dashboard",
    page_icon="🌤️",
)

st.title("🌤️ Weather Dashboard")


if st.button("Synchronize weather"):
    response = requests.post(
        f"{API_URL}/weather/sync",
        timeout=10,
    )

    response.raise_for_status()

    st.success("Weather synchronized.")


response = requests.get(
    f"{API_URL}/weather",
    timeout=10,
)

response.raise_for_status()

weather_records = response.json()


for weather in weather_records:
    st.subheader(
        f"{weather['city_name']}, {weather['country']}"
    )

    col1, col2 = st.columns(2)

    col1.metric(
        "Temperature",
        f"{weather['temperature']} °C",
    )

    col2.metric(
        "Humidity",
        f"{weather['humidity']} %",
    )

    st.write(
        f"**Weather:** {weather['desc_en']}"
    )

    st.divider()