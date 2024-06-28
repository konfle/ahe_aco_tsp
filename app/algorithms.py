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
    Implementation of ant colony optimisation for the traveling salesman problem.

    Args:
        distances (dict): Dictionary of distances between cities.
        num_ants (int): Number of ants.
        alpha (float): Pheromone influence factor for selecting the next city.
        beta (float): Coefficient of the effect of distance on the selection of the next city.
        evaporation_rate (float): The evaporation rate of the pheromone.
        max_iterations (int): Maximum number of iterations.
        max_stagnation_iterations (int): Maximum number of iterations without improving the best solution.

    Returns:
        tuple: A tuple containing the best solution and its length.
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
    Calculates the route length for a given solution.

    Args:
        path (list): List of cities in order of visit.
        distances (dict): Dictionary of distances between cities.

    Returns:
        float: The length of the route.
    """
    length = 0
    for i in range(len(path) - 1):
        length += distances[path[i]]["distances"][path[i + 1]]
    # Dodanie odległości z ostatniego do pierwszego miasta (powrót do punktu startowego)
    length += distances[path[-1]]["distances"][path[0]]

    return length
