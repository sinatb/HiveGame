import random
import numpy as np
import time


class Logger:
    def __init__(self, file_address, metadata_address):
        self.file_address = file_address
        self.metadata_address = metadata_address

        self.file = open(file_address, 'a')
        md = open(metadata_address, 'r')
        self.offset = int(md.readline())
        md.close()

    def log(self, h1, h2, state, winner):
        self.file.write(f'game {self.offset}\n')
        self.file.write('AI1 parameters: ')
        self.file.write(str.join(', ', map(str, h1)))
        self.file.write('\n')
        self.file.write('AI2 parameters: ')
        self.file.write(str.join(', ', map(str, h2)))
        self.file.write('\n')
        self.file.write('winner: ')
        self.file.write(str.join(', ', map(str, winner)))
        self.file.write('\n')
        self.file.write('\n')
        self.file.write(str(state))
        self.file.write('\n')
        self.file.write('\n')

        self.file.flush()
        self.offset += 1

    def flush(self):
        self.file.close()
        md = open(self.metadata_address, 'w')
        md.write(str(self.offset))
        md.write('\n')
        md.close()


def start_match(h1, h2, max_moves=80):  # returns winner
    return h1


def start_tournament(individuals):  # returns winner
    while len(individuals) > 1:
        winners = []

        winner_count = len(individuals) // 2

        for i in range(winner_count):
            h1 = individuals[i]
            h2 = individuals[i+winner_count]
            winners.append(start_match(h1, h2))

        individuals = winners

    return individuals[0]


LOGGER = Logger('logs.txt', 'metadata.txt')


def crossover_and_mutate(h1, h2):
    shuffled = list(range(len(h1)))
    random.shuffle(shuffled)

    child = [0.0 for _ in h1]

    for i in range(len(shuffled)):
        gene_index = shuffled[i]
        from_h1 = h1[gene_index]
        from_h2 = h2[gene_index]

        if i < len(shuffled) // 2:
            child[gene_index] = from_h1
        else:
            child[gene_index] = from_h2

    p = random.random()
    if p < 0.2:
        mutation_index = random.choice(shuffled)
        child[mutation_index] = child[mutation_index] * (random.random() + 0.5)

    return tuple(child)


def create_initial_population(size, chromosome_size, gene_max):
    pop = []
    for _ in range(size):
        pop.append(tuple(
            [gene_max * random.random() for _ in range(chromosome_size)]
        ))
    return pop


def next_generation(population):  # returns next generation
    k = 1 << ((len(population) // 2 - 1).bit_length())  # tournament size, must be power of 2
    parent_count = int(len(population) * 0.25)  # number of tournaments
    child_count = int(len(population) * 0.75)

    parents = []

    for i in range(parent_count):
        individuals = random.choices(population, k=k)
        winner = start_tournament(individuals)
        parents.append(winner)

    children = []
    for i in range(child_count):
        h1 = random.choice(parents)
        h2 = random.choice(parents)
        c = crossover_and_mutate(h1, h2)
        children.append(c)

    return parents + children


def save_pop_to_file(pop, file):
    for ind in pop:
        file.write(str.join(' ', map(str, ind)))
        file.write('\n')
    file.close()


def get_pop_from_file(file):
    r = list(
        map(lambda x: tuple(map(float, str.split(x, ' '))), file.readlines())
    )
    file.close()
    return r


def run():
    save_file_address = 'save.txt'
    population = get_pop_from_file(open(save_file_address, 'r'))
    if len(population) == 0:
        population = create_initial_population(32, 7, 12)

    max_iterations = 10
    max_iterations_after_convergence = 3
    last_std = -1
    i = 0

    for iteration in range(max_iterations):
        print(f'in iteration #{iteration}')
        print('creating next generation...')
        print()

        st = time.time()
        population = next_generation(population)
        print(f'created next generation in {round(st - time.time(), 2)}s')
        save_pop_to_file(population, open(save_file_address, 'w'))

        current_std = np.mean(np.std(population, axis=0))
        i += np.isclose(current_std, last_std, atol=0.1)

        if i == max_iterations_after_convergence:
            print('exiting because of convergence')
            break

        last_std = current_std
        print()

    LOGGER.flush()

