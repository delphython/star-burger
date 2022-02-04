import requests

from geopy import distance

from places.models import Place

from star_burger import settings


YANDEX_API_KEY = settings.YANDEX_API_KEY


def fetch_coordinates(address):
    place = Place.objects.filter(address=address).first()
    if place:
        return place.lat, place.lon
    else:
        coordinates = fetch_coordinates_from_yandex(address)
        if coordinates:
            lat, lon = coordinates
            Place.objects.create(
                address=address,
                lat=lat,
                lon=lon,
            )
            return lat, lon
        else:
            return None


def get_distance(address_from, address_to):
    coordinates_from = fetch_coordinates(address_from)
    coordinates_to = fetch_coordinates(address_to)
    if (coordinates_from is not None) & (coordinates_to is not None):
        return round(
            distance.distance(
                fetch_coordinates(address_from), fetch_coordinates(address_to)
            ).km,
            3,
        )
    else:
        return None


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
