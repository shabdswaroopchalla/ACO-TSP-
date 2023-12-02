import numpy as np


def calculate_distance(tour, distance_matrix):
    total_distance = 0
    num_cities = len(tour)

    for i in range(num_cities - 1):
        total_distance += distance_matrix[tour[i]][tour[i + 1]]

    # Add the distance from the last city back to the starting city
    total_distance += distance_matrix[tour[-1]][tour[0]]

    return total_distance


def initialize_pheromones(num_cities):
    return np.ones((num_cities, num_cities))


def update_pheromones(pheromone_matrix, ant_positions, ant_distances, evaporation_rate):
    pheromone_matrix *= (1 - evaporation_rate)  # Evaporation

    num_ants = len(ant_positions)

    for ant_index in range(num_ants):
        tour = ant_positions[ant_index]
        distance = ant_distances[ant_index]

        for i in range(len(tour) - 1):
            pheromone_matrix[tour[i]][tour[i + 1]] += 1 / distance

        # Update pheromone for the last edge connecting the last and first cities
        pheromone_matrix[tour[-1]][tour[0]] += 1 / distance

    return pheromone_matrix


def ant_colony_optimization(distance_matrix, num_ants, num_iterations, evaporation_rate=0.5, alpha=1, beta=2):
    num_cities = len(distance_matrix)

    # Initialize pheromone matrix
    pheromone_matrix = initialize_pheromones(num_cities)

    # Main optimization loop
    for iteration in range(num_iterations):
        # Initialize ant positions
        ant_positions = initialize_ants(num_ants, num_cities)

        # Move ants to construct solutions
        ant_positions, ant_distances = ant_movement(
            ant_positions, pheromone_matrix, distance_matrix, alpha, beta)

        # Update pheromones
        pheromone_matrix = update_pheromones(
            pheromone_matrix, ant_positions, ant_distances, evaporation_rate)

        # Find the best solution in this iteration
        best_solution_index = np.argmin(ant_distances)
        best_solution = ant_positions[best_solution_index]
        best_distance = ant_distances[best_solution_index]

        # Print best distance in each iteration (optional)
        print(f"Iteration {iteration + 1}: Best Distance = {best_distance}")

    # Return the best solution found
    return best_solution, best_distance


def initialize_ants(num_ants, num_cities):
    ant_positions = []

    for ant in range(num_ants):
        tour = np.random.permutation(num_cities)
        ant_positions.append(list(tour))

    return ant_positions


def ant_movement(ant_positions, pheromone_matrix, distance_matrix, alpha, beta):
    num_ants = len(ant_positions)
    ant_distances = []

    for ant_index in range(num_ants):
        tour = ant_positions[ant_index]
        distance = 0

        for i in range(len(tour) - 1):
            distance += distance_matrix[tour[i]][tour[i + 1]]

        # Add the distance for the last edge connecting the last and first cities
        distance += distance_matrix[tour[-1]][tour[0]]

        if distance != 0:
            ant_distances.append(distance)
        else:
            # Handle the case where the distance is zero
            ant_distances.append(float('inf'))

    return ant_positions, ant_distances


# Example usage
# Replace this with your actual distance matrix
distance_matrix = np.array([
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
])

num_ants = 5
num_iterations = 100
evaporation_rate = 0.5
alpha = 1
beta = 2

best_solution, best_distance = ant_colony_optimization(
    distance_matrix, num_ants, num_iterations, evaporation_rate, alpha, beta)

print("Best Solution:", best_solution)
print("Best Distance:", best_distance)
