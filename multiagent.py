import pygame, numpy as np


class Food:
    def __init__(self, resolution):
        self.eaten = False
        self.resolution = resolution
        self.SPEED = 0.5
        self.size = 18
        self.pos = [np.random.uniform(0.1 * self.resolution[0], 0.9 * self.resolution[0]),
                    np.random.uniform(0.1 * self.resolution[1], 0.9 * self.resolution[1])]

    def step(self, agents):
        closest_agent = None
        smallest_dist = np.inf
        for agent in agents:
            dist = ((agent.pos[0] - self.pos[0]) ** 2 + (agent.pos[1] - self.pos[1]) ** 2) ** 0.5
            if dist < smallest_dist:
                smallest_dist = dist
                closest_agent = agent

            if dist < agent.size:
                agent.hunger *= 0.9
                self.eaten = True

        self.pos[0] += (self.pos[0] - closest_agent.pos[0])/smallest_dist * self.SPEED
        self.pos[1] += (self.pos[1] - closest_agent.pos[1])/smallest_dist * self.SPEED

        if self.pos[0] < 0.1 * self.resolution[0]:
            self.pos[0] = 0.1 * self.resolution[0]
        if self.pos[0] > 0.9 * self.resolution[0]:
            self.pos[0] = 0.9 * self.resolution[0]
        if self.pos[1] < 0.1 * self.resolution[1]:
            self.pos[1] = 0.1 * self.resolution[1]
        if self.pos[1] > 0.9 * self.resolution[1]:
            self.pos[1] = 0.9 * self.resolution[1]

    def render(self, screen):
        random_val = np.random.uniform(0,100)
        pygame.draw.ellipse(screen, (255 - random_val, 255 - random_val, random_val), [self.pos[0], self.pos[1], self.size, self.size], 5)


class Agent:
    def __init__(self, resolution, size=25):
        self.MAX_SPEED = 1
        self.resolution = resolution
        self.pos = [np.random.uniform(0.1 * self.resolution[0], 0.9 * self.resolution[0]),
                    np.random.uniform(0.1 * self.resolution[1], 0.9 * self.resolution[1])]
        self.size = size
        self.speed = self.MAX_SPEED
        self.hunger = 1

    def step(self, foods, agents):
        closest_food = None
        smallest_dist = np.inf
        for food in foods:
            dist = ((food.pos[0] - self.pos[0]) ** 2 + (food.pos[1] - self.pos[1]) ** 2) ** 0.5
            if dist < smallest_dist:
                smallest_dist = dist
                closest_food = food

        if closest_food:
            self.pos[0] += (closest_food.pos[0] - self.pos[0])/smallest_dist * self.speed
            self.pos[1] += (closest_food.pos[1] - self.pos[1])/smallest_dist * self.speed

        # self.pos[0] += np.random.uniform(-1, 1) * self.speed
        # self.pos[1] += np.random.uniform(-1, 1) * self.speed

        # for agent in agents:
        #     dist = self.pos[0] - agent.pos[0]
        #     if abs(dist) < self.size:
        #         self.pos[0] = agent.pos[0] + self.size * np.sign(dist)
        #     dist = self.pos[1] - agent.pos[1]
        #     if abs(dist) < self.size:
        #         self.pos[1] = agent.pos[1] + self.size * np.sign(dist)

        if self.pos[0] < 0.1 * self.resolution[0]:
            self.pos[0] = 0.1 * self.resolution[0]
        if self.pos[0] > 0.9 * self.resolution[0]:
            self.pos[0] = 0.9 * self.resolution[0]
        if self.pos[1] < 0.1 * self.resolution[1]:
            self.pos[1] = 0.1 * self.resolution[1]
        if self.pos[1] > 0.9 * self.resolution[1]:
            self.pos[1] = 0.9 * self.resolution[1]
        self.speed = self.MAX_SPEED * self.hunger

    def render(self, screen):
        pygame.draw.rect(screen, (255 * (1 - self.hunger), 0,  255 * (1 - self.hunger)), [self.pos[0], self.pos[1], self.size, self.size],5)


class Env:
    def __init__(self):
        self.counter = 0
        self.resolution = (800, 800)
        self.background = (255, 255, 255)
        self.screen = pygame.display.set_mode(self.resolution)
        self.agents = []
        self.foods = []

    def reset(self):
        self.foods.clear()
        self.agents.clear()
        for _ in range(15):
            self.agents.append(Agent(self.resolution))
        for _ in range(15):
            self.foods.append(Food(self.resolution))

    def render(self):
        self.screen.fill(self.background)
        for food in self.foods:
            food.render(self.screen)
        for agent in self.agents:
            agent.render(self.screen)
        pygame.display.flip()

    def step(self):
        self.counter += 1
        if self.counter > 20:
            self.counter = 0
            self.foods.append(Food(self.resolution))
        for agent in self.agents:
            agent.step(self.foods, self.agents)
        for food in self.foods:
            if food.eaten:
                self.foods.remove(food)
            food.step(self.agents)


if __name__ == "__main__":
    env = Env()
    env.reset()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                env.reset()
        env.step()
        env.render()
