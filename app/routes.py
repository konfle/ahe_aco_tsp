import json
import folium
from flask import render_template, request, Blueprint, abort

from algorithms import ant_colony_optimization
from utils import load_data, calculate_distances

bp = Blueprint("routes", __name__)


@bp.route("/")
def index():
    """
    Renders the home page.

    Returns:
        str: Home page template.
    """
    return render_template("index.html")


@bp.route("/result", methods=["POST"])
def result():
    """
    Renders a page with the results of the ant algorithm.

    Returns:
        str: Results page template.
    """
    # Pobieranie parametrów z formularza
    num_ants = int(request.form["num_ants"])
    alpha = float(request.form["alpha"])
    beta = float(request.form["beta"])
    evaporation_rate = float(request.form["evaporation_rate"])
    max_iterations = int(request.form["max_iterations"])
    max_stagnation_iterations = int(request.form["max_stagnation_iterations"])

    # Pobieranie ścieżki do wybranego zestawu danych
    data_set_path = request.form["data_set"]

    # Wczytywanie danych i obliczanie odległości między miastami
    distances = load_data(data_set_path)
    distances = calculate_distances(distances)

    # Wywołanie algorytmu mrówkowego z nowymi danymi
    best_solution, best_solution_length = ant_colony_optimization(
        distances, num_ants, alpha, beta, evaporation_rate, max_iterations, max_stagnation_iterations
    )

    # Konwersja odległości na JSON
    distances_json = json.dumps(distances)

    return render_template("result.html",
                           solution=best_solution,
                           length=best_solution_length,
                           distances_json=distances_json)


@bp.route("/map", methods=["POST"])
def show_map():
    """
    Renders a map with the route of the comedian.

    Returns:
        str: Template for the map page.
    """
    # Pobieranie rozwiązania i odległości z formularza
    solution = request.form.get("solution")
    distances_json = request.form.get("distances")

    # Sprawdzenie, czy dane są dostępne
    if not solution or not distances_json:
        abort(404)

    # Przetwarzanie rozwiązania i odległości
    solution = solution.split(",")
    distances = json.loads(distances_json)
    solution.append(solution[0])

    # Wybór miasta początkowego i wyznaczenie jego współrzędnych
    start_city = solution[0]
    center_lat = distances[start_city]["lat"]
    center_lng = distances[start_city]["lng"]

    # Utworzenie mapy
    solution_map = folium.Map(location=[center_lat, center_lng], zoom_start=6)

    # Dodanie znaczników dla każdego miasta
    for city, data in distances.items():
        folium.Marker(location=[data["lat"], data["lng"]], popup=city).add_to(solution_map)

    # Rysowanie linii między miastami
    for i in range(len(solution) - 1):
        current_city = solution[i]
        next_city = solution[i + 1]

        # Wybór koloru linii w zależności od położenia
        if i == 0:
            color = "green"  # Pierwsze połączenie
        elif i == len(solution) - 2:
            color = "red"  # Ostatnie połączenie
        else:
            color = "blue"  # Połączenia pośrednie

        # Wyznaczenie współrzędnych punktu docelowego
        dest_lat = (distances[current_city]["lat"] + distances[next_city]["lat"]) / 2
        dest_lng = (distances[current_city]["lng"] + distances[next_city]["lng"]) / 2

        # Dodanie linii
        folium.PolyLine(locations=[[distances[current_city]["lat"], distances[current_city]["lng"]],
                                    [dest_lat, dest_lng]],
                        color=color).add_to(solution_map)

        folium.PolyLine(locations=[[dest_lat, dest_lng],
                                    [distances[next_city]["lat"], distances[next_city]["lng"]]],
                        color=color).add_to(solution_map)

    # Zapisanie mapy do pliku
    solution_map.save("templates/map.html")

    # Renderowanie szablonu z mapą
    return render_template("map.html")
