import numpy as np
from Colony import Colony
from ActionSpace import ActionSpace
from ObservationSpace import ObservationSpace


class Cure:
    # имитируемая колония бактерий или стая частиц
    bacteria: Colony
    # положение агента
    x: float
    y: float
    theta: float  # направление агента
    R: float  # область видимости агента
    n_bacteria: int  # сохраняем предыдущее значение количества видимых точек для расчета reward'a

    # конструктор
    def __init__(self, observation_r=5):
        self.bacteria = Colony()
        self.reward_range = (-1, 1)
        self.action_space = ActionSpace()
        self.observation_space = ObservationSpace()
        self.R = observation_r
        self.reset()

    #  Формирование вектора обзора observation.
    #  То что происходит в области видимости R от агента.
    def observe_area(self):
        # получим список соседей в радиусе R
        observe_bacteria = self.bacteria.observe(self.x, self.y, self.R)
        # получим список соседей в радиусе R*1.5
        observe_far_bacteria = self.bacteria.observe(self.x, self.y, self.R * 1.5)
        observe_far_bacteria = np.array(np.bitwise_and(observe_far_bacteria, np.invert(observe_bacteria)))

        observation = np.zeros(5)
        # подадим количество соседей
        n_bacteria = np.sum(observe_bacteria)
        observation[0] = n_bacteria / 20

        # посчитаем и подадим среднее направлений соседних бактерий
        sx = np.sum(np.cos(self.bacteria.theta[observe_bacteria]))
        sy = np.sum(np.sin(self.bacteria.theta[observe_bacteria]))
        observation[1] = np.arctan2(sy, sx) / np.pi
        # посчитаем и подадим среднее направление от агента до удаленных бактерий
        sx = np.sum(self.bacteria.x[observe_bacteria] - self.x)
        sy = np.sum(self.bacteria.y[observe_bacteria] - self.y)
        observation[2] = np.arctan2(sy, sx) / np.pi
        # посчитаем и подадим среднее направление от агента до удаленных бактерий
        sx = np.sum(self.bacteria.x[observe_far_bacteria] - self.x)
        sy = np.sum(self.bacteria.y[observe_far_bacteria] - self.y)
        observation[3] = np.arctan2(sy, sx) / np.pi
        if n_bacteria:
            observation[4] = self.theta / np.pi  # подадим направление агента
        return np.sum(observe_bacteria), observation

    # старт симуляции
    def reset(self):
        self.bacteria.reset()
        self.x = .5 * self.bacteria.area_size
        self.y = .5 * self.bacteria.area_size
        self.theta = ActionSpace().sample()
        self.n_bacteria, observation = self.observe_area()
        return observation

    # шаг симуляции
    def step(self, action):
        action = action * 3.2  # np.pi
        #  Для экономии времени при попадании на "чистую воду"
        #  просчитываем симуляцию не выпуская ее для обработки сети
        while True:
            # шаг симуляции бактерий
            self.bacteria.step()
            # шаг агента
            self.theta = np.sum(action)  # % (2*np.pi)
            self.x = self.x + self.bacteria.dt * self.bacteria.line_velocity * np.cos(self.theta)
            self.y = self.y + self.bacteria.dt * self.bacteria.line_velocity * np.sin(self.theta)
            self.x = self.x % self.bacteria.area_size
            self.y = self.y % self.bacteria.area_size
            # осматриваем окружение
            nBacteria, observation = self.observe_area()
            if np.sum(observation) != 0:
                break
            if self.n_bacteria > 0:
                break

        delta = nBacteria - self.n_bacteria
        if delta < 0:
            reward = 50 * delta / self.n_bacteria
        elif delta > 0 and self.n_bacteria:
            reward = 1 + delta
        elif nBacteria > 0:
            reward = 1
        elif nBacteria == 0:
            reward = 0
        else:
            reward = nBacteria

        # reward = nBacteria+3*reward
        done = nBacteria > self.bacteria.number_of_objects / 7
        self.n_bacteria = nBacteria
        return observation, reward, done, {}

    # получить координаты агента
    def get_position(self):
        return self.x, self.y, self.R

    # получить координаты всех бактерий
    def get_bacteria(self):
        return self.bacteria.get_bacteria()

    # отразить отладочную информацию
    def render(self, mode='human', close=False):
        # print(self.n_bacteria)
        pass

    # завершить симуляцию
    def close(self):
        pass
