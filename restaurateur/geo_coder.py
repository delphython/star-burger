import os

import requests

from dotenv import load_dotenv
from geopy import distance


load_dotenv()
YANDEX_API_KEY = os.environ["YANDEX_API_KEY"]


def get_distance(from_point, to_point):
    return round(
        distance.distance(
            fetch_coordinates(from_point), fetch_coordinates(to_point)
        ).km,
        3,
    )


def fetch_coordinates(address, apikey=YANDEX_API_KEY):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(
        base_url,
        params={
            "geocode": address,
            "apikey": apikey,
            "format": "json",
        },
    )
    response.raise_for_status()
    found_places = response.json()["response"]["GeoObjectCollection"][
        "featureMember"
    ]

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant["GeoObject"]["Point"]["pos"].split(" ")
    return lat, lon
