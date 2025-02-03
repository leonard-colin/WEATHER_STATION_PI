import requests
import os

LAT = os.environ.get("LATITUDE")
LON = os.environ.get("LONGITUDE")
CITY = os.environ.get("CITY")


def get_location():
    try:
        response = requests.get("http://ip-api.com/json/")
        data = response.json()
        if data["status"] == "success":
            return data["lat"], data["lon"], data["city"]
        else:
            return LAT, LON, CITY
    except Exception:
        return LAT, LON, CITY
