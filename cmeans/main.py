import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_blobs


class Point:
    def __init__(self, x, y, cluster=-1):
        self.x = x
        self.y = y
        self.cluster = cluster
        self.ps = None

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


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


def new_center(points):
    if points:
        x_center = np.mean(list(map(lambda p: p.x, points)))
        y_center = np.mean(list(map(lambda p: p.y, points)))
        center = Point(x_center, y_center)
    else:
        center = Point(0, 0)
    return center


def nearest_centroids(points, centers):
    for point in points:
        min_dist = dist(point, centers[0])
        point.cluster = 0
        for i in range(len(centers)):
            temp = dist(point, centers[i])
            if temp < min_dist:
                min_dist = temp
                point.cluster = i


def get_r_points(n, k):
    points = []
    X, y_true = make_blobs(n_samples=n, centers=k,
                           cluster_std=0.5, random_state=1)
    for xy in X:
        points.append(Point(xy[0], xy[1]))
    return points, y_true


def max_elem(matrix1, matrix2):
    new_matrix = np.zeros(shape=(len(matrix1), len(matrix1[0])))

    for i in range(len(matrix1)):
        for j in range(len(matrix1[0])):
            new_matrix[i][j] = abs(matrix1[i][j] - matrix2[i][j])
    return np.max(new_matrix)


def dist_to_clusters(points, centers, m=2):
    for point in points:
        ps = []
        for center in centers:
            if dist(point, center) <= 0.01:
                ps = point.ps
                break
            ps.append((1 / dist(point, center) ** (2 / (m - 1))))
        point.ps = ps
        point.cluster = np.argmax(ps)


def create_matrix(points, k):
    matrix = np.zeros(shape=(len(points), k))

    for i, point in enumerate(points):
        for j, p in enumerate(point.ps):
            matrix[i][j] = p
    return matrix


def dist(a, b):
    return np.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


if __name__ == "__main__":
    k = 3
    m = 2
    e = 0.001

    random_points = get_r_points(500, 3)[0]
    centers = centroids(random_points, k)
    dist_to_clusters(random_points, centers)
    p_matrix = create_matrix(random_points, k)
    past_matrix = np.zeros(shape=(len(random_points), k))

    iteration = 0
    while iteration < 100:
        print(iteration)
        print(max_elem(past_matrix, p_matrix))

        if max_elem(past_matrix, p_matrix) <= e:
            break

        past_matrix = p_matrix
        centers = []

        T_p_matrix = p_matrix.T
        for i in range(k):
            sum_of_p = 0
            sx = 0
            sy = 0
            for j, point in enumerate(random_points):
                sx += point.x * (T_p_matrix[i][j] ** m)
                sy += point.y * (T_p_matrix[i][j] ** m)
                sum_of_p += T_p_matrix[i][j] ** m
            centers.append(Point(sx / sum_of_p, sy / sum_of_p))

        dist_to_clusters(random_points, centers, k)
        p_matrix = create_matrix(random_points, k)

        iteration += 1
    clusters_points = [[] for _ in range(k)]

    for point in random_points:
        clusters_points[point.cluster].append(point)

    colors = []
    for cluster in clusters_points:
        p = plt.scatter(list(map(lambda l: l.x, cluster)), list(map(lambda l: l.y, cluster)), linewidths=3)
        colors.append(p.get_facecolor())

    for i, center in enumerate(centers):
        plt.scatter(center.x, center.y, linewidths=6, marker='v', color='black')

    plt.savefig("c_means.png")
    plt.show()
