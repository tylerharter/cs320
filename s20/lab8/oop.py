from matplotlib import pyplot as plt
import time

class Point:
    def __init__(self, x, y):
        self.create_time = time.time()
        self.x = x
        self.y = y

    def dist(self, other_pt):
        return ((self.x-other_pt.x) ** 2 + (self.y-other_pt.y) ** 2)**0.5

    def length(self):
        return self.dist(Point(0, 0))

    def __lt__(self, other_pt):
        return self.create_time < other_pt.create_time

    def __repr__(self):
        return "Point({}, {})".format(self.x, self.y)

class NamedPoint(Point):
    def __init__(self, x, y, name):
        Point.__init__(self, x, y)
        self.name = name

    def draw(self, ax):
        ax.text(self.x, self.y, self.name)

    def __repr__(self):
        return "NamedPoint({}, {}, {})".format(self.x, self.y, self.name)

n = NamedPoint(0.5, 0.9, "North")
s = NamedPoint(0.5, 0.1, "South")
e = NamedPoint(0.9, 0.5, "East")
w = NamedPoint(0.1, 0.5, "West")
points = sorted([e, s, w, n])

ax = plt.subplot()
for p in points:
    print(p)
    p.draw(ax)