import os

import requests

from dotenv import load_dotenv
from geopy import distance

from places.models import Place


load_dotenv()
YANDEX_API_KEY = os.environ["YANDEX_API_KEY"]


def fetch_coordinates(address):
    place = Place.objects.filter(address=address).first()
    if place:
        return (place.lat, place.lon)
    else:
        lat, lon = fetch_coordinates_from_yandex(address)
        save_place(address, lat, lon)
        return (lat, lon)


def get_distance(address_from, address_to):
    return round(
        distance.distance(
            fetch_coordinates(address_from), fetch_coordinates(address_to)
        ).km,
        3,
    )


def fetch_coordinates_from_yandex(address, apikey=YANDEX_API_KEY):
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


def save_place(address, lat, lon):
    place = Place.objects.create(
        address=address,
        lat=lat,
        lon=lon,
    )
    return place