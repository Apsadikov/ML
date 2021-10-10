import matplotlib.pyplot as plt
import numpy as np

class Point:
    def __init__(self, x, y, cluster=-1):
        self.x = x
        self.y = y
        self.cluster = cluster


def dist(a, b):
    return np.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


def get_random_points(n):
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

def recalculate_centroids(points, centroids, u, m):
    new_centroids = []
    for j in range(len(centroids)):
        num1 = 0.0
        num2 = 0.0
        den = 0.0
        for i in range(len(points)):
            num1 += (u[j][i] ** m) * points[i].x
            num2 += (u[j][i] ** m) * points[i].y
            den += u[j][i] ** m
        new_centroids.append(Point(num1 / den, num2 / den))
    return new_centroids

def check_func(new_u, old_u, eps):
    temp_u = []
    for i in range(len(new_u)):
        for j in range(len(new_u[i])):
            temp_u.append(abs(new_u[i][j] - old_u[i][j]))
    return max(temp_u) < eps

def get_coefficient(points, centroids, m):
    u = np.empty(shape=(len(centroids), len(points)))
    for i in range(len(centroids)):
        for j in range(len(points)):
            result = dist(points[j], centroids[i]) ** (2 / (1 - m))
            temp = 0.0
            for n in range(len(centroids)):
                temp += dist(points[j], centroids[n]) ** (2 / (1 - m))
            u[i][j] = result / temp
    return u

if __name__ == "__main__":
    n = 100  # точек
    k = 3  # кластеров
    m: float = 2
    eps: float = 0.01
    points = get_random_points(n)
    centers = centroids(points, k)
    plt.scatter(list(map(lambda p: p.x, points)), list(map(lambda p: p.y, points)), s=[2] * len(points))
    plt.scatter(list(map(lambda p: p.x, centers)), list(map(lambda p: p.y, centers)), color='r')
    plt.show()
    plt.close()
    old_u = get_coefficient(points, centers, m)
    while True:
        new_centers = recalculate_centroids(points, centers, old_u, m)
        new_u = get_coefficient(points, new_centers, m)
        if check_func(new_u, old_u, eps):
            break
        old_u = new_u
        centers = new_centers
    plt.scatter(list(map(lambda p: p.x, points)), list(map(lambda p: p.y, points)), s=[2] * len(points))
    plt.scatter(list(map(lambda p: p.x, centers)), list(map(lambda p: p.y, centers)), color='r')
    plt.show()
    plt.close()