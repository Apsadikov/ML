import matplotlib.pyplot as plt
import numpy as np


class Point:
    def __init__(self, x, y, cluster=-1):
        self.x = x
        self.y = y
        self.cluster = cluster


def dist(a, b):
    return np.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


def rand_points(n):
    points = []
    for i in range(n):
        point = Point(np.random.randint(0, 100), np.random.randint(0, 100))
        points.append(point)
    return points


def centroids(points, k):
    x_center = np.mean(list(map(lambda p: p.x, points)))
    y_center = np.mean(list(map(lambda p: p.y, points)))
    center = Point(x_center, y_center)
    R = max(map(lambda r: dist(r, center), points))
    centers = []
    for i in range(k):
        x_c = x_center + R * np.cos(2 * np.pi * i / k)
        y_c = y_center + R * np.sin(2 * np.pi * i / k)
        centers.append(Point(x_c, y_c))
    return centers


def nearest_centroids(points, centroids):
    for point in points:
        min_dist = dist(point, centroids[0])
        point.cluster = 0
        for i in range(len(centroids)):
            temp = dist(point, centroids[i])
            if temp < min_dist:
                min_dist = temp
                point.cluster = i


def recalculate_centroid(points, index):
    cluster_points = []
    for point in points:
        if point.cluster == index:
            cluster_points.append(point)
    x_center = np.mean(list(map(lambda p: p.x, cluster_points)))
    y_center = np.mean(list(map(lambda p: p.y, cluster_points)))
    center = Point(x_center, y_center)
    return center


if __name__ == "__main__":
    n = 100  # кол-во точек
    k = 5  # кол-во кластеров
    iterations = 100  # кол-во итераций
    points = rand_points(n)
    centers = centroids(points, k)

    for i in range(iterations):
        # Для каждой точки находим ближайший центроид
        nearest_centroids(points, centers)
        for j in range(k):
            # Перемещаем каждый центроид в центр точек, которые мы отнесли к этому центроиду
            centers[j] = recalculate_centroid(points, j)

    plt.scatter(list(map(lambda p: p.x, points)), list(map(lambda p: p.y, points)))
    plt.scatter(list(map(lambda p: p.x, centers)), list(map(lambda p: p.y, centers)))
    plt.show()
