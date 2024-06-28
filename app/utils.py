import json
import math


def load_data(data_set_path):
    """
   Loads data from a JSON file.

    Args:
        data_set_path (str): Path to the JSON file.

    Returns:
        dict: Data loaded from the JSON file.
    """
    with open(data_set_path, "r", encoding="utf-8") as file:
        return json.load(file)


def haversine(lat1, lon1, lat2, lon2):
    """
    Calculates the distance between two points with given geographical coordinates (latitude and longitude).

    Args:
        lat1 (float): Latitude of the first point in degrees.
        lon1 (float): Longitude of the first point in degrees.
        lat2 (float): Latitude of the second point in degrees.
        lon2 (float): Longitude of the second point in degrees.

    Returns:
        float: Distance between points in kilometres.
    """
    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Latitude and longitude differences
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Distance calculation
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    radius_of_earth = 6371  # Radius of the Earth in kilometers
    distance = radius_of_earth * c

    return distance


def calculate_distances(cities):
    """
    Calculates the distances between all pairs of cities using the haversine function and stores them in the dictionary.

    Args:
        cities (dict): A dictionary of cities containing their geographical coordinates.

    Returns:
        dict: An updated dictionary of cities containing the distances between them.
    """
    for city1, data1 in cities.items():
        for city2, data2 in cities.items():
            if city1 != city2:
                # Calculating distances using the haversine function
                dist = haversine(data1["lat"], data1["lng"], data2["lat"], data2["lng"])
                # Recording distances in the city dictionary
                data1["distances"][city2] = dist

    return cities
