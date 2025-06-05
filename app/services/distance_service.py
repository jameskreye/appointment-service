import requests
from math import radians, cos, sin, sqrt, asin

def get_coordinates(zipcode, country='us'):
    response = requests.get(f'https://api.zippopotam.us/{country}/{zipcode}')
    if response.status_code != 200:
        return None
    data = response.json()
    lon = float(data['places'][0]['longitude'])
    lat = float(data['places'][0]['latitude'])
    return lat, lon

def calculate_distance(coord1, coord2):
    # Haversine Formula
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    r = 6371  # Radius of Earth in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return r * c  # Distance in KM

