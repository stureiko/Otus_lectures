import numpy as np


# Имитация роевого поведения
class Colony:
    # положения частицы
    x: np.ndarray
    y: np.ndarray
    # угол направления частицы
    theta: np.ndarray
    # скорость частицы по осям
    vx: np.ndarray
    vy: np.ndarray

    # Конструктор
    def __init__(self, number_of_objects=200, line_velocity=3, area_size=60, dt=.2, radius=5, eta=.5):
        self.number_of_objects = number_of_objects  # количество бактерий
        self.area_size = area_size  # размер области (L)
        self.dt = dt  # фаза /скорость
        self.line_velocity = line_velocity  # линейная скорость
        self.radius = radius  # радиус взаимодействия
        self.eta = eta  # случайный угол отклонения (в радианах)
        self.reset()

    # расстановка n частиц на площадке LxL
    def reset(self):
        # положения частиц
        self.x = np.random.rand(self.number_of_objects, 1) * self.area_size
        self.y = np.random.rand(self.number_of_objects, 1) * self.area_size
        # направление и осевые скорости частиц относительно
        # постоянной линейной скорости v0
        self.theta = 2 * np.pi * np.random.rand(self.number_of_objects, 1)
        self.vx = self.line_velocity * np.cos(self.theta)
        self.vy = self.line_velocity * np.sin(self.theta)

    # Шаг имитации
    def step(self):
        # движение
        self.x += self.vx * self.dt
        self.y += self.vy * self.dt
        # применение периодических пограничных условий
        self.x = self.x % self.area_size
        self.y = self.y % self.area_size
        # найти средний угол соседей в диапазоне R
        mean_theta = self.theta
        for b in range(self.number_of_objects):
            neighbors = (self.x - self.x[b]) ** 2 + (self.y - self.y[b]) ** 2 < self.radius ** 2
            sx = np.sum(np.cos(self.theta[neighbors]))
            sy = np.sum(np.sin(self.theta[neighbors]))
            mean_theta[b] = np.arctan2(sy, sx)
        # добавление случайного отклонения
        self.theta = mean_theta + self.eta * (np.random.rand(self.number_of_objects, 1) - 0.5)
        # изменение скорости
        self.vx = self.line_velocity * np.cos(self.theta)
        self.vy = self.line_velocity * np.sin(self.theta)
        return self.theta

    # Получить список частиц внутри радиуса r от координат x, y
    def observe(self, x, y, r):
        return (self.x - x) ** 2 + (self.y - y) ** 2 < r ** 2

    # Вывести координаты частицы i
    def print(self, i):
        return print(self.x[i], self.y[i])

    # Получить координаты частиц
    def get_bacteria(self):
        return self.x, self.y

    # Получить массив направлений частиц
    def get_theta(self):
        return self.theta
