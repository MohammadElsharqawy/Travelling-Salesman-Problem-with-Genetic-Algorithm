import random, math


def generate_random_paths(total_destinations): 
    random_paths = []
    for _ in range(20000):
        random_path = list(range(1, total_destinations))
        random.shuffle(random_path)
        random_path = [0] + random_path
        random_paths.append(random_path)
    return random_paths


#evolove this intial population through a number of generations and each time we fet closer to the final solutoin. 
# a) survivors, get the population, pass it through some sort of a filter, and choose the remaining survivors
# b)cross over, get these survivors and combine them togetther to produce new solutions 
# c) apply mutations to our solution.
# repeatedly do this, finally fet the survival of the fittest, cross over and mutatin we have new production


def total_distance(distance, path):
    return sum([distance[path[i-1]][path[i]]  for i in range(1, len(path))])


def choose_survivors(distance, old_generation):
    survivors = []
    random.shuffle(old_generation)
    mid = len(old_generation) // 2
    for i in range(mid):
       if total_distance(distance, old_generation[i]) < total_distance(distance, old_generation[i+mid]):
           survivors.append(old_generation[i])
       else:
           survivors.append(old_generation[i+mid])    
    return survivors


# create offsprings, divide them 2 groups, should random start and end from one and put their values in the second and vice versa.

def create_offsprings(parent_a, parent_b):
    offspring = []

    start = random.randint(0, len(parent_a)-1)
    end = random.randint(start, len(parent_a)-1)

    sub_path_from_a = parent_a[start:end]
    remaining_path_from_b = list(item for item in parent_b if item not in sub_path_from_a)

    for i in range(len(parent_a)):
        if start <= i <= end and len(sub_path_from_a)>0 :
             offspring.append(sub_path_from_a.pop(0))
        else:
            offspring.append(remaining_path_from_b.pop(0))
    return offspring

def apply_crossover(survivors):
    offspprings = []
    mid = len(survivors) //2
    for i in range(mid):
        parent_a , parent_b = survivors[i], survivors[i+1]
        for _ in range(2):
            offspprings.append(create_offsprings(parent_a, parent_b))
            offspprings.append(create_offsprings(parent_b, parent_a))
    return offspprings        


#apply mutation on a small percentage of population

def apply_mutations(generation):
    gen_wt_mutations = []
    for path in generation:
        if random.randint(0, 1000) < 9:
            index1, index2 = random.randint(1, len(path) - 1), random.randint(1, len(path) - 1)
            path[index1], path[index2] = path[index2], path[index1]
        gen_wt_mutations.append(path)
    return gen_wt_mutations



def generate_new_population(distance, old_generation):
    survivors = choose_survivors(distance, old_generation)
    crossovers = apply_crossover(survivors)
    new_population = apply_mutations(crossovers)
    return new_population



def choose_best(distance, paths, count):
    return sorted(paths, key=lambda path: total_distance(distance, path))[:count]


def choose_worst(distance, paths, count):
    return sorted(paths, reverse=True, key=lambda path: total_distance(distance, path))[:count]


if __name__ == '__main__':
    total_iterations = 500
    evolvedIterations = []

    alphaToNum = {"#":0, "A":1, "B":2, "C":3, "D":4, "E":5, "F":6, "G":7, "H":8}
    distance = []

    for i in range(9):
        row  = []
        for j in range(9):
            row.append(float("inf"))
        distance.append(row)

    distance[alphaToNum["#"]][alphaToNum["#"]] = 0
    distance[alphaToNum["#"]][alphaToNum["A"]] = 3
    distance[alphaToNum["#"]][alphaToNum["C"]] = 2
    distance[alphaToNum["#"]][alphaToNum["G"]] = 5

    distance[alphaToNum["A"]][alphaToNum["A"]] = 0
    distance[alphaToNum["A"]][alphaToNum["#"]] = 3
    distance[alphaToNum["A"]][alphaToNum["C"]] = 6

    distance[alphaToNum["B"]][alphaToNum["B"]] = 0
    distance[alphaToNum["B"]][alphaToNum["C"]] = 9
    distance[alphaToNum["B"]][alphaToNum["D"]] = 9

    distance[alphaToNum["C"]][alphaToNum["C"]] = 0
    distance[alphaToNum["C"]][alphaToNum["A"]] = 6
    distance[alphaToNum["C"]][alphaToNum["#"]] = 2
    distance[alphaToNum["C"]][alphaToNum["F"]] = 4
    distance[alphaToNum["C"]][alphaToNum["B"]] = 9

    distance[alphaToNum["D"]][alphaToNum["D"]] = 0
    distance[alphaToNum["D"]][alphaToNum["B"]] = 8
    distance[alphaToNum["D"]][alphaToNum["E"]] = 7
    distance[alphaToNum["D"]][alphaToNum["H"]] = 9

    distance[alphaToNum["E"]][alphaToNum["E"]] = 0
    distance[alphaToNum["E"]][alphaToNum["F"]] = 2
    distance[alphaToNum["E"]][alphaToNum["D"]] = 7
    distance[alphaToNum["E"]][alphaToNum["G"]] = 1
    distance[alphaToNum["E"]][alphaToNum["H"]] = 1

    distance[alphaToNum["F"]][alphaToNum["F"]] = 0
    distance[alphaToNum["F"]][alphaToNum["C"]] = 4
    distance[alphaToNum["F"]][alphaToNum["E"]] = 2

    distance[alphaToNum["G"]][alphaToNum["G"]] = 0
    distance[alphaToNum["G"]][alphaToNum["#"]] = 5
    distance[alphaToNum["G"]][alphaToNum["E"]] = 1
    distance[alphaToNum["G"]][alphaToNum["H"]] = 3

    distance[alphaToNum["H"]][alphaToNum["H"]] = 0
    distance[alphaToNum["H"]][alphaToNum["D"]] = 9
    distance[alphaToNum["H"]][alphaToNum["E"]] = 1
    distance[alphaToNum["H"]][alphaToNum["G"]] = 3


    evolvedIterations.append(generate_random_paths(len(distance)))
    for _ in range(total_iterations):
        evolvedIterations.append(generate_new_population(distance, evolvedIterations[-1]))

    for p in range(total_iterations):
        population = evolvedIterations[p]
        minimum = math.inf
        for path in population:
            minimum = min(minimum, total_distance(distance, path))
        print(minimum if minimum != float("inf") else "NOT Feasible")
