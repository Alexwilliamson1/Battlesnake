import game_simulator
import random
import copy
import statistics
import json

POPULATION_SIZE = 25
GENERATIONS = 30
ELITE = 4
MUTATION_RATE = 0.2
MUTATION_SCALE = 0.1

next_id = 0

#To initialize a Battlesnake population with random genomes, run tournaments for each generation, and evolve the population:
def genetic_algorithm():
    population = intitialize_population()
    total_game_count = 0
    for generation in range(GENERATIONS):
        print(f"{generation}/{GENERATIONS} generations have been evolved.",)
        run_tournament(population, generation, total_game_count)
        population, elite = evolve(population)

#To simulate games between two Battlesnakes with evolving genomes and two Battlesnakes with simplified genomes:
def run_tournament(population, generation, total_game_count):        
        game_count = 0
        turn_count = 0
        binomial_coefficient = (POPULATION_SIZE * (POPULATION_SIZE - 1))//2
        bots1 = [bot_genome1() for _ in range(2)]
        bots2 = [bot_genome2() for _ in range(2)]
        bots = bots1 + bots2
        for i in range(len(population)):
            population[i]["id"] = new_id()
            population[i]["generation"] = generation
        for i in range(len(population)):
            for j in range(i + 1, len(population)):
                if (game_count == 0):
                        print(f"{game_count}/{binomial_coefficient * GENERATIONS}} games have been played.")
                genome_a = population[i]
                genome_b = population[j]
                genome_c = bot_genome1()
                genome_d = bot_genome2()
                winner, turns = game_simulator.run_game([genome_a["weights"], genome_b["weights"], genome_c, genome_d], seed=total_game_count)
                #print("The number of turns survived by each player are: " + str(turns))
                if winner == 0:
                    genome_a["stats"]["wins"] += 1
                    genome_b["stats"]["losses"] += 1
                elif winner == 1:
                    genome_b["stats"]["wins"] += 1
                    genome_a["stats"]["losses"] += 1
                else:
                    genome_b["stats"]["losses"] += 1
                    genome_a["stats"]["losses"] += 1

                genome_a["stats"]["turns"] += turns[0]
                genome_b["stats"]["turns"] += turns[1]
                genome_a["stats"]["games"] += 1
                genome_b["stats"]["games"] += 1
                game_count += 1
                if (game_count % 20 == 0):
                        print(f"{game_count}/{binomial_coefficient * GENERATIONS} games have been played.")
                total_game_count += 1
                turn_count += max(turns[0], turns[1])   
        for k in range(len(population)):
            population[k]["fitness"] = fitness(population[k]["stats"])
            population[k]["avg_turns"] = population[k]["stats"]["turns"] / population[k]["stats"]["games"]
            
        log_stats(population, generation, game_count, turn_count)

#To create a new population from the best-performing Battlesnakes in the previous population and by randomly selecting and mutating "parent" genomes:
def evolve(population):
        original_population = population[:]
        population.sort(key=lambda g: g["fitness"], reverse=True)
        next_population = [copy.deepcopy(g) for g in population[:ELITE]]
        for i in range(len(next_population)):
            next_population[i]["stats"] = {"wins": 0, "losses": 0, "turns": 0, "games": 0}
            next_population[i]["fitness"] = 0 
            next_population[i]["avg_turns"] = 0
        first_elite = copy.deepcopy(next_population[0])
        first_elite_weights = first_elite["weights"]

        while len(next_population) < POPULATION_SIZE:
            p1 = select_parent(original_population)
            p2 = select_parent(original_population)
            child = empty_genome()
            child_weights = crossover(p1["weights"], p2["weights"])
            mutate(child_weights)
            child["weights"] = child_weights
            next_population.append(child)

        population = next_population
        return population, first_elite_weights

#The following function logs statistics about the best-performing genome from each population both in the console and in a file named "elites.jsonl."  It also logs statistics about each generation in a file named "generations.jsonl":
def log_stats(population, generation, game_count, turn_count):
        best_genome = max(population, key=lambda g: g["fitness"])
        with open("elites.jsonl", "a") as f:
            f.write(json.dumps({
                "generation": generation,
                "genome": best_genome["id"],
                "fitness": best_genome["fitness"],
                "weights": best_genome["weights"]
            }) + "\n\n")

        print("\nThe Battlesnake from generation " + str(generation) + " with the highest fitness score is: " + str(best_genome) + "\n")

        generation_summary = {
                "generation": generation,
                "max_fitness": max(g["fitness"] for g in population),
                "mean_fitness": statistics.mean(g["fitness"] for g in population),                                
                "std_fitness": statistics.stdev(g["fitness"] for g in population),
                "avg_game_length": turn_count / game_count,
        }

        with open("generations.jsonl", "a") as f:
            f.write(json.dumps({
                "generation": generation,
                "max_fitness": generation_summary["max_fitness"],
                "mean_fitness": generation_summary["mean_fitness"],
                "std_fitness": generation_summary["std_fitness"],
                "avg_game_length": generation_summary["avg_game_length"]
            }) + "\n\n")

#A genome with semi-random weights and fields for counting wins, losses, etc.:
def random_genome():
    return {
        "id": None,
        "generation": 0,
        "weights": {
           "territory": random.uniform(0, 80),
           "accessible_area": random.uniform(0, 1.2),
           "max_future_area": random.uniform(0, 2),
           "length": random.uniform(0, 30),
           "if_reachable_food": random.uniform(0, 600),
           "closest_food": random.uniform(0, 10),
           "hunger_factor": -1,
           "if_no_reachable_food": random.uniform(-400, 0),
           "smaller_opponent_dist1": random.uniform(0, 500),
           "smaller_opponent_dist2": random.uniform(0, 500),
           "smaller_opponent_dist3": random.uniform(0, 400),
           "larger_opponent_dist1": random.uniform(-500, 0),
           "larger_opponent_dist2": random.uniform(-500, 0),
           "reachable_tail": random.uniform(0, 500),
           "unreachable_tail1": random.uniform(-500, 0),
           "unreachable_tail2": random.uniform(-400, 0),
           "random_variability": 0,
           "victory": 1_000_000,
        },
        "stats": {
            "wins": 0,
            "losses": 0,
            "turns": 0, 
            "games": 0
        },
        "fitness": 0,
        "avg_turns": 0,
    }

#A genome with all variable fields set to zero:
def empty_genome():
    return {
        "id": None,
        "generation": 0,
        "weights": {
           "territory": 0,
           "accessible_area": 0,
           "max_future_area": 0,
           "length": 0,
           "if_reachable_food": 0,
           "closest_food": 0,
           "hunger_factor": -1,
           "if_no_reachable_food": 0,
           "smaller_opponent_dist1": 0,
           "smaller_opponent_dist2": 0,
           "smaller_opponent_dist3": 0,
           "larger_opponent_dist1": 0,
           "larger_opponent_dist2": 0,
           "reachable_tail": 0,
           "unreachable_tail1": 0,
           "unreachable_tail2": 0,
           "random_variability": 0,
           "victory": 1_000_000,
        },
        "stats": {
            "wins": 0,
            "losses": 0,
            "turns": 0, 
            "games": 0
        },
        "fitness": 0,
        "avg_turns": 0,
    }

#The following is a simplified genome that only scores proximity to food objects and opponents and victory.  It also adds a very small random number to the score.
def bot_genome1():
    return {
       "territory": 0,
       "accessible_area": 0,
       "max_future_area": 0,
       "length": 0,
       "if_reachable_food": 30,
       "closest_food": 0,
       "hunger_factor": 1,
       "if_no_reachable_food": 0,
       "smaller_opponent_dist1": 0,
       "smaller_opponent_dist2": 15,
       "smaller_opponent_dist3": 0,
       "larger_opponent_dist1": -10,
       "larger_opponent_dist2": 0,
       "reachable_tail": 0,
       "unreachable_tail1": 0,
       "unreachable_tail2": 0,
       "random_variability": 0.01,
       "victory": 1_000_000,
    }

#A second simplified genome:
def bot_genome2():
    return {
       "territory": 0,
       "accessible_area": 0.2,
       "max_future_area": 0,
       "length": 0,
       "if_reachable_food": 13,
       "closest_food": 0,
       "hunger_factor": 1,
       "if_no_reachable_food": 0,
       "smaller_opponent_dist1": 4,
       "smaller_opponent_dist2": 3,
       "smaller_opponent_dist3": 1,
       "larger_opponent_dist1": -4,
       "larger_opponent_dist2": 0,
       "reachable_tail": 0,
       "unreachable_tail1": 0,
       "unreachable_tail2": 0,
       "random_variability": 0.01,
       "victory": 1_000_000,
    }


def fitness(results):
    return (
        results["wins"] * 1 +
        results["turns"] * 0 - 
        results["losses"] * 1
    )

def intitialize_population():  
    #[bot_genome() for _ in range(POPULATION_SIZE / 2)]  
    return [random_genome() for _ in range(POPULATION_SIZE)]

def mutate(weights):
    WEIGHT_RANGES = {
        "territory": (0, 80),
        "accessible_area": (0, 1.2),
        "max_future_area": (0, 2),
        "length": (0, 30),
        "if_reachable_food": (0, 600),
        "closest_food": (0, 10),
        "if_no_reachable_food": (-400, 0),
        "smaller_opponent_dist1": (0, 500),
        "smaller_opponent_dist2": (0, 500),
        "smaller_opponent_dist3": (0, 400),
        "larger_opponent_dist1": (-500, 0),
        "larger_opponent_dist2": (-500, 0),
        "reachable_tail": (0, 500),
        "unreachable_tail1": (-500, 0),
        "unreachable_tail2": (-400, 0),
    }
    
    for key, (low, high) in WEIGHT_RANGES.items():
        if random.random() < MUTATION_RATE:
            span = high - low
            delta = random.uniform(-MUTATION_SCALE, MUTATION_SCALE) * span
            weights[key] += delta

            weights[key] = max(low, min(high, weights[key]))
    
    assert weights["if_no_reachable_food"] <= 0
    assert weights["larger_opponent_dist1"] <= 0
    assert weights["victory"] == 1_000_000

def select_parent(population, k=4):
    contenders = random.sample(population, k)
    return max(contenders, key=lambda g: g["fitness"])

def crossover(w1, w2):
    child = {}
    for key in w1:
        child[key] = random.choice([w1[key], w2[key]])
    return child

def new_id():
    global next_id
    gid = f"g{next_id}"
    next_id += 1
    return gid

genetic_algorithm()
