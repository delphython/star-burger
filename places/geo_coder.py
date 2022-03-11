import requests

from geopy import distance

from places.models import Place

from django.conf import settings


YANDEX_API_KEY = settings.YANDEX_API_KEY


def fetch_coordinates(address):
    coordinates = fetch_coordinates_from_yandex(address)
    lat, lon = coordinates if coordinates else None
    Place.objects.create(
        address=address,
        lat=lat,
        lon=lon,
    )
    return lat, lon


def get_distance(address_from, address_to, places):
    address_from_in_places = [
        item for item in places if item["address"] == address_from
    ]
    address_to_in_places = [
        item for item in places if item["address"] == address_to
    ]
    coordinates_from = (
        (address_from_in_places[0]["lat"], address_from_in_places[0]["lon"])
        if address_from_in_places
        else fetch_coordinates(address_from)
    )
    coordinates_to = (
        (address_to_in_places[0]["lat"], address_to_in_places[0]["lon"])
        if address_to_in_places
        else fetch_coordinates(address_to)
    )
    if any(coordinates_from) & any(coordinates_to):
        return round(
            distance.distance(coordinates_from, coordinates_to).km,
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
