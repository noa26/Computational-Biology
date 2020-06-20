from shapely.geometry.polygon import Polygon
from typing import List


class Square:
	def __init__(self, x: int, y: int):
		self.x: int = x
		self.y: int = y
		self.polygon: Polygon = Polygon([(x, y), (x, y + 1), (x + 1, y + 1), (x + 1, y)])

	def __eq__(self, other):
		if self.coordinates() == other.coordinates():
			return True
		return False

	def coordinates(self):
		return self.x, self.y


class SquareMap:
	def __init__(self):
		self.squares = dict()
		for s in create_squares():
			self.squares[(s.x, s.y)] = s

	def get_locations(self):
		return list(self.squares.keys())

	def get_neighbors(self, h: (int, int)) -> List[Square]:
		if h not in list(self.squares.keys()):
			return []
		diff = [(1, 0), (1, 1), (1, -1),
				(0, 1), (0, -1),
				(-1, 0), (-1, 1), (-1, -1)]
		# diff = [(1, 0), (-1, 0), (0, 1), (0, -1)]
		neighbors = [(h[0] + x, h[1] + y) for x, y in diff]
		return [self.squares[n] for n in neighbors if n in list(self.squares.keys())]


def create_squares(count=36, max_row=6):
	locations = []
	i = 0
	while len(locations) < count:
		for j in range(max_row):
			locations.append((i, j))
		i += 1
	return [Square(*l) for l in locations]
