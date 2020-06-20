import numpy as np
from typing import List
from hex_map import SquareMap

N = 36
MAX_DEPTH = 2
ALPHA = 0.25


def distance1(m1: np.ndarray, m2: np.ndarray):
	return np.linalg.norm(m1 - m2)


class KohonenMap(SquareMap):

	def __init__(self, distance=distance1):
		SquareMap.__init__(self)
		self.neurons: List[(np.ndarray, (int, int))] = []
		self.distance = distance

		# create random neurons
		for location in self.get_locations():
			self.neurons.append((np.random.randint(low=0, high=2,
													size=(10, 10), dtype=int), location))

	def draw_neurons(self) -> None:
		pass

	def update_neuron(self, v: np.ndarray, index: int, d: int, t: int):
		"""
		:param v: the sample to adjust according to.
		:param index: neuron's index
		:param d: depth from the original neuron
		:param t: time
		:return: None
		"""
		neuron: np.ndarray = self.neurons[index][0]

		c = KohonenMap.learning_rate(t) * KohonenMap.neighborhood(d)
		neuron = neuron + ALPHA * c * (v - neuron)

		self.neurons[index] = (neuron, self.neurons[index][1])
		if d < MAX_DEPTH:
			# update all of the neighbors
			for i in self.neighbors_indices(self.neurons[index][1]):
				self.update_neuron(v, i, d + 1, t)

	@staticmethod
	def neighborhood(d):
		return np.exp(-d/MAX_DEPTH)

	@staticmethod
	def learning_rate(t):
		return np.exp(-t/1000)

	def neighbors_indices(self, h):
		locations = [(n.x, n.y) for n in self.get_neighbors(h)]
		neighbors_i = []
		i = 0
		for n in self.neurons:
			if n[1] in locations:
				neighbors_i.append(i)
			i += 1
		return neighbors_i

	def map_sample(self, sample: np.ndarray, d, t):
		# the closest neuron's index
		n_0 = self.closest(sample)
		self.update_neuron(sample, n_0, d, t)
		pass

	def closest(self, v: np.ndarray) -> int:
		distances = [self.distance(v, n) for n, _ in self.neurons]
		return int(np.argmin(distances))

	def get_clusters(self, data):
		digits = [int(i / 10) for i in range(len(data))]
		labeled = list(zip(data, digits))

		clusters = [[] for _ in range(len(self.neurons))]

		for sample in labeled:
			index = self.closest(sample[0])
			clusters[index].append(sample[1])

		return clusters

	def __getitem__(self, index: (int, int)) -> np.ndarray:
		for n in self.neurons:
			if n[1] == index:
				return n[0]
		return None

	def __setitem__(self, key: (int, int), value: np.ndarray) -> bool:
		index = 0
		for n in self.neurons:
			if n[1] == key:
				self.neurons[index] = (value, n[1])
				return True
			index += 1
		return False


def save(m: KohonenMap, filename='neurons.npz'):
	arrays = [n[0] for n in m.neurons]
	np.savez(filename, *arrays)


def reload(m: KohonenMap, filename='neurons.npz'):
	arrays = []
	dt_container = np.load(filename)
	keys = ['arr_' + str(i) for i in range(0, 36)]

	for k in keys:
		arrays.append(dt_container[k])

	for i in range(len(m.neurons)):
		n = m.neurons[i]
		m.neurons[i] = (arrays[i], n[1])
