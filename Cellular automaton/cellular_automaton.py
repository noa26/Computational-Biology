"""
Corona Cellular Automaton.

"""
import numpy as np
import random
from organism import states, Organism

MAX_NEIGHBORS = 8


class CellularAutomaton:

    def __init__(self, n=200, m=200, p=0.5, k=0):
        self.N = n
        self.M = m
        self.P = p
        self.K = k
        self.automaton = np.zeros((self.N, self.M))
        self.organisms = []
        self.infected_count = 0

    def add_organisms(self, n):
        if n == 0:
            return
        if n > self.N * self.M:
            raise ValueError("\nOverpopulated environment.\nChoose different N value.")

        # generate n different locations.
        locations = set([(random.randrange(self.N), random.randrange(self.M)) for _ in range(n)])
        while len(locations) < n:
            locations.add((random.randrange(self.N), random.randrange(self.M)))

        # make one infected
        locations = list(locations)
        location = random.choice(locations)
        locations.remove(location)
        self.organisms.append(Organism(location[0], location[1], states['infected']))
        self.infected_count += 1

        # add healthy organism
        for location in locations:
            self.organisms.append(Organism(location[0], location[1], states['healthy']))

        self._update_automaton()

    def move_all(self, times=1):
        for o in self.organisms:
            action = random.choice(o.actions(self))
            self._move(o, action)

    def update_states(self):
        if self.K == MAX_NEIGHBORS:
            return
        for o in self.organisms:
            if not o.is_healthy():
                continue
            neighbors = []
            locations = self.neighbors_locations(o)[:(MAX_NEIGHBORS - self.K)]
            for x, y in locations:
                neighbors.append(Organism(x, y, self.automaton[x][y]))
            o.update_state(neighbors, self)
        self._update_automaton()

    def neighbors_locations(self, o):
        locations = [((o.row + i) % self.N, (o.column + j) % self.M)
                     for i in range(-1, 2) for j in range(-1, 2)]
        return [(x, y) for x, y in locations if x != o.row or y != o.column]

    def all_infected(self):
        print("self.organisms:", len(self.organisms), "self.infected_count:", self.infected_count)
        if len(self.organisms) == self.infected_count:
            return True
        return False

    def _update_automaton(self):
        self.automaton = np.zeros((self.N, self.M))
        for o in self.organisms:
            self.automaton[o.row, o.column] = o.state

    def _move(self, o, location):
        if self.automaton[location[0]][location[1]] != states['empty']:
            return
        self.automaton[o.row][o.column] = states['empty']

        o.row, o.column = location
        self.automaton[o.row][o.column] = o.state


def parameters_check(n, m, p, k, num):
    errors = [message for (has_error, message) in (
        (n < 1 or m < 1, 'dimensions must be positive'),
        (int(n) != n or int(m) != m, 'dimensions must be integers'),
        (num > n * m, 'N > n * m'),
        (num < 1, "N must be positive"),
        (int(num) != num, "N must be an integer"),
        (p < 0 or p > 1, 'P must be a float between 0 and 1'),
        (k > 8, 'K limit is 8'),
        (k < 0, 'K minimum value is 0')
    ) if has_error]

    return errors






















