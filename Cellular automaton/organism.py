"""
organism class.
Represent living beings in a "living" environment.
"""

states = {'empty': 0, 'healthy': 1, 'infected': 2}


class Organism:

    def __init__(self, row, column, state):
        self.row = row
        self.column = column
        if state in states.values():
            self.state = state
        else:
            self.state = states['empty']

    def actions(self, ca):
        acts = []
        neighbors = ca.neighbors(self)
        for neighbor in neighbors:
            if ca.automaton[neighbor[0]][neighbor[1]] == states['empty']:
                acts.append(neighbor)

        # add staying in place action
        acts.append((self.row, self.column))
        return acts

    def update_state(self, neighbors, ca):
        if self.state != states['healthy']:
            return
        for neighbor in neighbors:
            if neighbor.state == states['infected']:
                self.state = states['infected']
                ca.infected_count += 1
                break

    def __eq__(self, other):
        if self.row == other.row and self.column == other.column:
            return True
        return False
