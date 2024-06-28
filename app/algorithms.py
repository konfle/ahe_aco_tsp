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
                probabilities = []  # List of probabilities of selecting the next city
                total_probability = 0.0

                # Calculating the probabilities of an ant selecting the next city
                for next_city in cities:
                    if next_city not in visited_cities:
                        pheromone = pheromones[cities.index(current_city)][
                            cities.index(next_city)]  # Pheromone concentration on a given route
                        distance = distances[current_city]["distances"][
                            next_city]  # Distance between the current city and the next city
                        # Heuristics - the smaller the distance, the greater the heuristic value
                        heuristic = 1.0 / distance
                        probability = (pheromone ** alpha) * (
                                    heuristic ** beta)  # Calculation of the probability of choosing a given city
                        probabilities.append(
                            (next_city, probability))  # Adding a pair (city, probability) to the list
                        total_probability += probability  # Update the sum of probabilities

                # Normalization of probabilities
                probabilities = [(city, prob / total_probability) for city, prob in probabilities]
                selected_next_city = random.choices(
                    [city for city, _ in probabilities],
                    weights=[prob for _, prob in probabilities]
                )[0]  # Selection of the next city based on weights

                visited_cities.append(selected_next_city)
                current_city = selected_next_city

            current_solution = visited_cities
            current_solution_length = calculate_path_length(current_solution, distances)

            if current_solution_length < best_solution_length:
                best_solution = current_solution
                best_solution_length = current_solution_length

            # Adding pheromones based on the current solution of a given ant
            for i in range(num_cities):
                current_city = current_solution[i]
                next_city = current_solution[(i + 1) % num_cities]
                pheromones[cities.index(current_city)][cities.index(next_city)] += 1.0 / current_solution_length

        # Pheromone update along the route of the best solution
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
    # Adding the distance from the last city to the first city (return to the starting point)
    length += distances[path[-1]]["distances"][path[0]]

    return length
