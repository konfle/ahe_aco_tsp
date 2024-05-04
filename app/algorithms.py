import random
import numpy as np


def ant_colony_optimization(distances,
                            num_ants,
                            alpha,
                            beta,
                            evaporation_rate,
                            max_iterations,
                            max_stagnation_iterations):
    """
    Implementacja optymalizacji kolonii mrówek dla problemu komiwojażera.

    Args:
        distances (dict): Słownik odległości między miastami.
        num_ants (int): Liczba mrówek.
        alpha (float): Współczynnik wpływu feromonu na wybór kolejnego miasta.
        beta (float): Współczynnik wpływu odległości na wybór kolejnego miasta.
        evaporation_rate (float): Współczynnik parowania feromonu.
        max_iterations (int): Maksymalna liczba iteracji.
        max_stagnation_iterations (int): Maksymalna liczba iteracji bez poprawy najlepszego rozwiązania.

    Returns:
        tuple: Krotka zawierająca najlepsze rozwiązanie i jego długość.
    """
    cities = list(distances.keys())
    num_cities = len(cities)
    pheromones = np.ones((num_cities, num_cities))
    best_solution = None
    best_solution_length = float("inf")
    stagnation_count = 0

    while stagnation_count < max_stagnation_iterations:
        for ant in range(num_ants):
            current_city = random.choice(cities)
            visited_cities = [current_city]

            while len(visited_cities) < num_cities:
                probabilities = []  # Lista prawdopodobieństw wyboru kolejnego miasta
                total_probability = 0.0

                # Obliczanie prawdopodobieństw wyboru kolejnego miasta przez mrówkę
                for next_city in cities:
                    if next_city not in visited_cities:
                        pheromone = pheromones[cities.index(current_city)][
                            cities.index(next_city)]  # Stężenie feromonu na danej trasie
                        distance = distances[current_city]["distances"][
                            next_city]  # Odległość między aktualnym a następnym miastem
                        heuristic = 1.0 / distance  # Heurystyka - im mniejsza odległość, tym większa wartość heurystyki
                        probability = (pheromone ** alpha) * (
                                    heuristic ** beta)  # Obliczenie prawdopodobieństwa wyboru danego miasta
                        probabilities.append(
                            (next_city, probability))  # Dodanie pary (miasto, prawdopodobieństwo) do listy
                        total_probability += probability  # Aktualizacja sumy prawdopodobieństw

                # Normalizacja prawdopodobieństw
                probabilities = [(city, prob / total_probability) for city, prob in probabilities]
                selected_next_city = random.choices(
                    [city for city, _ in probabilities],
                    weights=[prob for _, prob in probabilities]
                )[0]  # Wybór kolejnego miasta na podstawie wag

                visited_cities.append(selected_next_city)
                current_city = selected_next_city

            current_solution = visited_cities
            current_solution_length = calculate_path_length(current_solution, distances)

            if current_solution_length < best_solution_length:
                best_solution = current_solution
                best_solution_length = current_solution_length

            # Dodawanie feromonów na podstawie aktualnego rozwiązania danej mrówki
            for i in range(num_cities):
                current_city = current_solution[i]
                next_city = current_solution[(i + 1) % num_cities]
                pheromones[cities.index(current_city)][cities.index(next_city)] += 1.0 / current_solution_length

        # Aktualizacja feromonów na trasie najlepszego rozwiązania
        for i in range(num_cities):
            current_city = best_solution[i]
            next_city = best_solution[(i + 1) % num_cities]
            pheromones[cities.index(current_city)][cities.index(next_city)] += 1.0 / best_solution_length

        stagnation_count += 1

    return best_solution, best_solution_length


def calculate_path_length(path, distances):
    """
    Oblicza długość trasy dla danego rozwiązania.

    Args:
        path (list): Lista miast w kolejności odwiedzania.
        distances (dict): Słownik odległości między miastami.

    Returns:
        float: Długość trasy.
    """
    length = 0
    for i in range(len(path) - 1):
        length += distances[path[i]]["distances"][path[i + 1]]
    # Dodanie odległości z ostatniego do pierwszego miasta (powrót do punktu startowego)
    length += distances[path[-1]]["distances"][path[0]]

    return length
