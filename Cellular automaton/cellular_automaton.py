"""
Corona Cellular Automaton.

"""
import numpy as np
import random
from organism import states, Organism


class CellularAutomaton:

    def __init__(self, n=200, m=200):
        self.N = n
        self.M = m
        self.automaton = np.zeros((self.N, self.M))
        self.organisms = []
        self.infected_count = 0
        print("shape", self.automaton.shape)

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
        location = locations.pop()
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

    def neighbors(self, o):
        locations = [((o.row + i) % self.N, (o.column + j) % self.M)
                     for i in range(-1, 2) for j in range(-1, 2)]
        return [(x, y) for x, y in locations if x != o.row or y != o.column]

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
