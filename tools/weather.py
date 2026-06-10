import requests
from langchain.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get the current weather in a given city.
    
    Args:
        city (str): The city to get the weather for.

    Returns:
        dict: The weather in the city.

    """
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
        geo_data = requests.get(geo_url).json()

        if not geo_data.get("results"):
            return {"error" : f"City {city} not found"}

        location = geo_data["results"][0]
        latitude, longitude = location["latitude"], location["longitude"]

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,weather_code"
        weather_data = requests.get(weather_url).json()

        current_weather = weather_data["current"]["temperature_2m"]
        return f"The current weather in {city} is {current_weather} degrees Celsius"

    except Exception as e:
        return {"error" : f"Error fetching weather data: {e}"}