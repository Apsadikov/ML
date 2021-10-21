import numpy as np
import pygame


class DBScan:
    def recalculate(self, points, epsilon):
        labels = [0] * len(points)
        cluster_id = 0
        minimum_points = 1
        for i in range(0, len(points)):
            if not (labels[i] == 0):
                continue
            near_points = self.near_by_points(points, i, epsilon)
            if len(near_points) < minimum_points:
                labels[i] = -1
            else:
                cluster_id += 1
                labels[i] = cluster_id
                i = 0
                while i < len(near_points):
                    point = near_points[i]
                    if labels[point] == -1:
                        labels[point] = cluster_id

                    elif labels[point] == 0:
                        labels[point] = cluster_id
                        point_near = self.near_by_points(points, point, epsilon)
                        if len(point_near) >= minimum_points:
                            near_points = near_points + point_near
                    i += 1
        return labels

    def near_by_points(self, points, point_id, epsilon):
        near = []
        for point_ids in range(0, len(points)):
            if np.linalg.norm(points[point_id] - points[point_ids]) < epsilon:
                near.append(point_ids)
        return near

    def colors(self, color_id):
        if color_id == 1:
            return (255, 0, 0)
        if color_id == 2:
            return (0, 255, 0)
        if color_id == 3:
            return (0, 0, 255)
        if color_id == 4:
            return (0, 0, 0)
        return (125, 125, 125)

    def draw(self, color_id, clusters):
        for point, cluster in zip(color_id, clusters):
            color = self.colors(cluster)
            radius = 10
            pygame.draw.circle(window, color, point, radius)


if __name__ == '__main__':
    pygame.init()
    dbscan = DBScan()
    window = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    points = []
    window.fill((255, 255, 255))

    epsilon = 30

    done = False
    while not done:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                points.append(pygame.mouse.get_pos())
                window.fill((255, 255, 255))
                prediction = dbscan.recalculate(np.array(points), epsilon)
                dbscan.draw(points, prediction)

        pygame.display.update()
