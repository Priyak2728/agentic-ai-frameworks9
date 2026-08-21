from mcp.server.fastmcp import FastMCP
import requests

mcp = FastMCP("WeatherServer")

@mcp.tool()
def get_weather(city: str) -> str:
    """
    Get current weather for a city.
    """

    geo = requests.get(
        f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    ).json()

    if "results" not in geo:
        return "City not found"

    lat = geo["results"][0]["latitude"]
    lon = geo["results"][0]["longitude"]

    weather = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    ).json()

    current = weather["current_weather"]

    return (
        f"Temperature: {current['temperature']}°C, "
        f"Wind Speed: {current['windspeed']} km/h"
    )

if __name__ == "__main__":
    mcp.run()