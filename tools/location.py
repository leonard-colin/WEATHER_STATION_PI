import requests
import os
from dotenv import load_dotenv

load_dotenv()

LAT = os.environ.get("LATITUDE")
LON = os.environ.get("LONGITUDE")
CITY = os.environ.get("CITY")
is_location_enabled = os.environ.get("ENABLE_WEATHER_LOCATION")


def get_location():
    if is_location_enabled:
        try:
            response = requests.get("http://ip-api.com/json/")
            data = response.json()
            if data["status"] == "success":
                return data["lat"], data["lon"], data["city"]
            else:
                return LAT, LON, CITY
        except Exception:
            return LAT, LON, CITY

    return LAT, LON, CITY
