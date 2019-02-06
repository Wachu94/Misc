import numpy as np, pygame, pickle, sys
from generative_models.common import setup_weights, forward_prop, activate
from generative_models.optimizers import SGD, Adam
from generative_models.figures import square

def save(data, name="save"):
    with open(name + ".p", 'wb') as file:
        pickle.dump(data, file)

def load(name):
    try:
        with open(name + ".p", 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        return None

class display:
    def __init__(self, x, y, side):
        self.pixels = []
        for i in range(side):
            for j in range(side):
                self.pixels.append(square(x + j, y + i, 10, offset=0))

    def draw(self, screen):
        for pixel in self.pixels:
            pixel.draw(screen)

    def set_pixel_values(self, vector):
        assert len(vector) == len(self.pixels)
        for i, pixel in enumerate(self.pixels):
            value = int((1 - vector[i]) * 255)
            pixel.color = (value, value, value)

A = [[0, 1, 1, 1, 0],
     [1, 0, 0, 0, 1],
     [1, 1, 1, 1, 1],
     [1, 0, 0, 0, 1],
     [1, 0, 0, 0, 1]]
side = len(A)
A = np.ravel(A)

B = [[1, 1, 1, 0, 0],
     [1, 0, 0, 1, 0],
     [1, 1, 1, 1, 1],
     [1, 0, 0, 0, 1],
     [1, 1, 1, 1, 0]]
B = np.ravel(B)

C = [[0, 1, 1, 1, 0],
     [1, 0, 0, 0, 0],
     [1, 0, 0, 0, 0],
     [1, 0, 0, 0, 0],
     [0, 1, 1, 1, 0]]
C = np.ravel(C)

D = [[1, 1, 1, 1, 0],
     [1, 0, 0, 0, 1],
     [1, 0, 0, 0, 1],
     [1, 0, 0, 0, 1],
     [1, 1, 1, 1, 0]]
D = np.ravel(D)

E = [[1, 1, 1, 1, 1],
     [1, 0, 0, 0, 0],
     [1, 1, 1, 0, 0],
     [1, 0, 0, 0, 0],
     [1, 1, 1, 1, 1]]
E = np.ravel(E)

F = [[1, 1, 1, 1, 1],
     [1, 0, 0, 0, 0],
     [1, 1, 1, 0, 0],
     [1, 0, 0, 0, 0],
     [1, 0, 0, 0, 0]]
F = np.ravel(F)

G = [[0, 1, 1, 1, 0],
     [1, 0, 0, 0, 0],
     [1, 0, 1, 1, 1],
     [1, 0, 0, 0, 1],
     [0, 1, 1, 1, 0]]
G = np.ravel(G)

H = [[1, 0, 0, 0, 1],
     [1, 0, 0, 0, 1],
     [1, 1, 1, 1, 1],
     [1, 0, 0, 0, 1],
     [1, 0, 0, 0, 1]]
H = np.ravel(H)

X = [A, B, C, D, E, F, G, H]

extraction_weights = load("ExtractionWeights")
generation_weights = load("GenerationWeights")

# extraction_weights = setup_weights((len(A), 512, 2))
# generation_weights = setup_weights((2, 512, len(A)))
weights = []
for weight in extraction_weights:
    weights.append(weight)
for weight in generation_weights:
    weights.append(weight)

lr = 1e-10
activation = "ELU"
weights = Adam(X, weights, epochs=int(1e4), lr=lr, activation=activation)
save(weights[:len(extraction_weights)], "ExtractionWeights")
save(weights[len(extraction_weights):], "GenerationWeights")

extraction_weights = load("ExtractionWeights")
generation_weights = load("GenerationWeights")

temp = forward_prop(X, extraction_weights, activation=activation)
min_x = min(temp[:,0])
max_x = max(temp[:,0])
min_y = min(temp[:,1])
max_y = max(temp[:,1])

displays = []

display_side = 15

for r in range(display_side):
    for c in range(display_side):
        current_display = display(6 * r + 1, 6 * c + 1, 5)
        Y = forward_prop([(max_x - min_x)/(display_side - 1) * r + min_x, (max_y - min_y)/(display_side - 1) * c + min_y], generation_weights, activation=activation)
        Y = activate(Y, "Sigmoid")
        current_display.set_pixel_values(Y)
        displays.append(current_display)
screen = pygame.display.set_mode((1000,1000))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    screen.fill((255, 255, 255))
    for display in displays:
        display.draw(screen)
    pygame.display.flip()


