from shapely.geometry import Polygon


class Region:
    """
    This class defines a region.
    Every region is defines by name, shape and color.
    color - a tuple of fill color and border color.
    """

    def __init__(self, name: str, shape, color=("w", "k")):
        self.name = name
        self.shape = shape
        self.neighbors = set()
        self.color = color


class ColoredMap:
    """
    This class defines a Colored Map.
    The map is a set of Polygons called regions. (each with a unique name/ID/index)
    Each region can be colored.
    If not specified a region's color is white with black edges.
    """

    def __init__(self):
        self.regions = dict()

    def add_region(self, region: Region):
        self.regions[region.name] = region

    def show_map(self, canvas):
        for region in self.regions.values():
            canvas.fill(*region.shape.exterior.xy, color=region.color[0])
            canvas.plot(*region.shape.exterior.xy, color=region.color[1])


def load_polygons(filename):
    import csv
    shapes = dict()
    with open(filename, "r+") as f:
        reader = csv.reader(f, delimiter=",")
        for row in reader:
            points = list()
            for p in row[1:]:
                points.append([float(i) for i in p.split(" ")])
            shapes[row[0]] = Polygon(points)
    return shapes


def default_map(filename="polygons.csv"):
    colored_map = ColoredMap()
    shapes = load_polygons(filename)

    for s in shapes:
        r = Region(s, shapes[s])
        colored_map.add_region(r)
    return colored_map


def main():
    import matplotlib.pyplot as plt

    cmap = default_map()
    cmap.show_map(plt)

    plt.show()


if __name__ == "__main__":
    main()
