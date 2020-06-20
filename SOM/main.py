import re
import numpy as np
import matplotlib.pyplot as plt
import sys
from som import KohonenMap, distance1, save, reload
from matplotlib.colors import LinearSegmentedColormap

norm = plt.Normalize(0, 1)
tuples = list(zip(map(norm, [0, 1]), ['white', 'brown']))
CMAP = LinearSegmentedColormap.from_list("", tuples)
EPOCHS = 10


def string_to_array(s):
	return np.array([np.fromstring(row, dtype='u1') - ord('0') for row in s.split("\n")])


def load_data(filename: str = "Digits_Ex3.txt") -> list:
	with open(filename, "r") as f:
		data = re.split("\n\n|\n \n", f.read())
		samples = [s.strip() for s in data]
		digits = []

		for s in samples:
			digits.append(string_to_array(s))

		return digits


def QE(m: KohonenMap):
	data = load_data()
	avg_dist = 0
	for sample in data:
		avg_dist += m.distance(sample, m.neurons[m.closest(sample)][0])

	return avg_dist / len(data)


def TE(m:KohonenMap):
	data = load_data()
	bad_mapping_count = 0

	for sample in data:
		distances = [m.distance(sample, neuron[0]) for neuron in m.neurons]
		min1, min2 = 0, 1
		if distances[min1] > distances[min2]:
			min1, min2 = 1, 0

		# find two closest
		for i in range(len(distances)):
			if distances[i] < distances[min1]:
				min1 = i
			elif distances[i] < distances[min2]:
				min2 = i

		# check neighborhood
		if min1 not in m.neighbors_indices(m.neurons[min2][1]):
			bad_mapping_count += 1

	return bad_mapping_count


def train_map(m, plot=False, ax=None):
	data = load_data()
	t = 0
	for i in range(EPOCHS):
		np.random.shuffle(data)
		for sample in data:
			m.map_sample(sample, 0, t)
			t += 1
			if ax is not None and plot and t % 20 == 0:
				for value, (x, y) in m.neurons:
					ax[x, y].pcolormesh(value, vmin=0, vmax=1, cmap=CMAP)
				plt.draw()
				plt.pause(0.0001)


def main():

	plot = False
	train = False
	np = True

	argv = sys.argv
	if '-train' in argv:
		train = True
	if '-plot' in argv:
		plot = True
	if '-np' in argv:
		np = False

	m = KohonenMap()

	fig1, ax = plt.subplots(6, 6)
	# fig2, ax2 = plt.subplots(1, 1) # axis for u-matrix
	# ax2.invert_yaxis()

	for a in ax.flatten():
		a.invert_yaxis()
		a.axes.yaxis.set_visible(False)
		a.axes.xaxis.set_visible(False)
	ax = ax.transpose()

	# training net or loading a saved one.
	if train:
		train_map(m, plot=plot, ax=ax)
	else:
		reload(m, filename='best_map.npz')

	# draw neurons
	clusters = m.get_clusters(load_data())
	i = 0
	count = 0
	for value, (x, y) in m.neurons:
		minimum, maximum = 0, 1
		maximum = 10 / max(1, len(clusters[i]) + 1)
		if len(clusters[i]) > 0:
			count += 1
		ax[x, y].pcolormesh((value >= 0.6).astype(int), vmin=minimum, vmax=maximum, cmap=CMAP)
		i += 1

	qe, te = QE(m), TE(m)
	print("QE\t\tTE")
	print("\t".join([str(float(int(qe*100)) / 100), str(te)]))
	print('-' * 100)

	i = 0
	for sample in load_data():
		if i % 10 == 0:
			print()
			print('\'', int(i / 10), '\' neurons location:')
		print(m.neurons[m.closest(sample)][1], end=', ')
		i += 1
	print('\n' + '-' * 100)

	# # create u-matrix
	# matrix = np.zeros((6, 6), dtype=float)
	#
	# for x, y in [(col, row) for col in range(6) for row in range(6)]:
	# 	neighbors = m.neighbors_indices((x, y))
	# 	avg = sum([distance1(m[x, y], m.neurons[n][0]) for n in neighbors])
	# 	avg = avg / len(neighbors)
	# 	matrix[x][y] = -avg
	#
	# matrix = matrix - min(matrix.flatten())
	# matrix /= matrix.sum(axis=1)[:, np.newaxis]
	# ax2.pcolormesh(matrix, shading='gouraud',cmap=CMAP, vmin=min(matrix.flatten()), vmax=max(matrix.flatten()))
	if np:
		plt.show()


def best_maps():
	m = KohonenMap()
	train_map(m, plot=False)
	qe, te = QE(m), TE(m)
	print("\t".join([str(qe), str(te)]))
	print("done")


if __name__ == '__main__':
	main()
