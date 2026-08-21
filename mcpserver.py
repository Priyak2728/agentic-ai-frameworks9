from mcp.server.fastmcp import FastMCP
import requests

mcp = FastMCP("Weather-MCP")


@mcp.tool()# user-->AI-->MCP tool-->external system
def get_weather(city: str) -> str:
    """
    Get current weather for a city.
    Uses Open-Meteo (free API, no API key required).
    """

    # Convert city to coordinates
    geo_url = (
        f"https://geocoding-api.open-meteo.com/v1/search"
        f"?name={city}&count=1"
    )

    geo_response = requests.get(geo_url).json()

    if "results" not in geo_response:
        return f"Could not find city: {city}"

    lat = geo_response["results"][0]["latitude"]
    lon = geo_response["results"][0]["longitude"]

    # Get current weather
    weather_url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}"
        f"&longitude={lon}"
        f"&current_weather=true"
    )

    weather_response = requests.get(weather_url).json()

    current = weather_response["current_weather"]

    return (
        f"Weather in {city}\n"
        f"Temperature: {current['temperature']}°C\n"
        f"Wind Speed: {current['windspeed']} km/h"
    )


if __name__ == "__main__":

    print("Testing MCP Tool...\n")

    print(get_weather("mumbai"))

    print("\nMCP Server Running...")

    mcp.run()