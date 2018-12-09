import numpy as np, pygame, random, time

class Agent:
    size = 20
    def __init__(self, pos, value):
        self.pos = pos
        self.value = value
        # self.po = random.random()
        # self.psp = random.random()
        self.po = 0
        self.psp = 1

    def render(self, screen):
        color_value = ((self.value + 1) * 255)//2
        pygame.draw.rect(screen, (color_value, color_value, color_value),
                         [self.pos[0]*self.size, self.pos[1]*self.size, self.size, self.size])

class Env:
    def __init__(self):
        self.resolution = (800, 800)
        self.background = (255, 255, 255)
        self.screen = pygame.display.set_mode(self.resolution)
        self.agents = [[None for _ in range(self.resolution[0]//Agent.size)] for _ in range(self.resolution[1]//Agent.size)]

    def reset(self):
        for r in range(len(self.agents)):
            for c in range(len(self.agents[0])):
                # self.agents[r][c] = Agent((r, c), (random.randint(0, 1) * 2) - 1)
                self.agents[r][c] = Agent((r, c), random.randint(-1, 1))

    def render(self):
        self.screen.fill(self.background)
        for row in self.agents:
            for agent in row:
                agent.render(self.screen)
        pygame.display.flip()

    def step(self):
        # for r in range(1, len(self.agents) - 3):
        j = random.randint(1, len(self.agents) - 3)
        i = random.randint(1, len(self.agents[0]) - 3)
        a = self.agents[j][i]
        b = self.agents[j][i + 1]
        c = self.agents[j + 1][i]
        d = self.agents[j + 1][i + 1]
        if a == b:
            if a.psp > self.agents[j][i - 1].po:
                self.agents[j][i - 1].value = a.value
            if b.psp > self.agents[j][i + 2].po:
                self.agents[j][i + 2].value = b.value
        else:
            if b.psp > self.agents[j][i - 1].po:
                self.agents[j][i - 1].value = b.value
            if a.psp > self.agents[j][i + 2].po:
                self.agents[j][i + 2].value = a.value

        if a == c:
            if a.psp > self.agents[j - 1][i].po:
                self.agents[j - 1][i].value = a.value
            if c.psp > self.agents[j + 2][i].po:
                self.agents[j + 2][i].value = c.value
        else:
            if c.psp > self.agents[j - 1][i].po:
                self.agents[j - 1][i].value = c.value
            if a.psp > self.agents[j + 2][i].po:
                self.agents[j + 2][i].value = a.value

        if c == d:
            if c.psp > self.agents[j + 1][i - 1].po:
                self.agents[j + 1][i - 1].value = c.value
            if d.psp > self.agents[j + 1][i + 2].po:
                self.agents[j + 1][i + 2].value = d.value
        else:
            if d.psp > self.agents[j + 1][i - 1].po:
                self.agents[j + 1][i - 1].value = d.value
            if c.psp > self.agents[j + 1][i + 2].po:
                self.agents[j + 1][i + 2].value = c.value

        if b == d:
            if b.psp > self.agents[j - 1][i + 1].po:
                self.agents[j - 1][i + 1].value = b.value
            if d.psp > self.agents[j + 2][i + 1].po:
                self.agents[j + 2][i + 1].value = d.value
        else:
            if d.psp > self.agents[j - 1][i + 1].po:
                self.agents[j - 1][i + 1].value = d.value
            if b.psp > self.agents[j + 2][i + 1].po:
                self.agents[j + 2][i + 1].value = b.value


        # magnetisation = 0
        # undecided = 0
        # for row in self.agents:
        #     for agent in row:
        #         if agent.value == 0:
        #             undecided += 1
        #         magnetisation += agent.value
        # print("Undecided:", undecided)
        # print("Magnetisation:", magnetisation)


if __name__ == "__main__":
    env = Env()
    env.reset()
    counter = 0
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                env.reset()
        env.step()
        counter += 1
        if counter == 100:
            counter = 0
            env.render()


