import json
import math


def load_data(data_set_path):
    """
    Wczytuje dane z pliku JSON.

    Args:
        data_set_path (str): Ścieżka do pliku JSON.

    Returns:
        dict: Dane wczytane z pliku JSON.
    """
    with open(data_set_path, "r", encoding="utf-8") as file:
        return json.load(file)


def haversine(lat1, lon1, lat2, lon2):
    """
    Oblicza odległość między dwoma punktami o zadanych współrzędnych geograficznych (szerokość i długość).

    Args:
        lat1 (float): Szerokość geograficzna pierwszego punktu w stopniach.
        lon1 (float): Długość geograficzna pierwszego punktu w stopniach.
        lat2 (float): Szerokość geograficzna drugiego punktu w stopniach.
        lon2 (float): Długość geograficzna drugiego punktu w stopniach.

    Returns:
        float: Odległość między punktami w kilometrach.
    """
    # Konwersja stopni na radiany
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Różnice szerokości i długości geograficznych
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Obliczanie odległości
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    radius_of_earth = 6371  # Promień Ziemi w kilometrach
    distance = radius_of_earth * c

    return distance


def calculate_distances(cities):
    """
    Oblicza odległości między wszystkimi parami miast za pomocą funkcji haversine i zapisuje je w słowniku.

    Args:
        cities (dict): Słownik miast zawierający ich współrzędne geograficzne.

    Returns:
        dict: Zaktualizowany słownik miast zawierający odległości między nimi.
    """
    for city1, data1 in cities.items():
        for city2, data2 in cities.items():
            if city1 != city2:
                # Obliczanie odległości za pomocą funkcji haversine
                dist = haversine(data1["lat"], data1["lng"], data2["lat"], data2["lng"])
                # Zapisywanie odległości w słowniku miast
                data1["distances"][city2] = dist

    return cities
