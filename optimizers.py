import random, numpy as np
from tqdm import trange
from generative_models.common import calculate_gradient

def SGD(X, weights, activation="ReLU", lr=1e-2, mini_batch=500, epochs=10, logits=True, show_progress_bar=True):
    if show_progress_bar:
        progress_bar = trange(epochs)
    else:
        progress_bar = range(epochs)
    for _ in progress_bar:

        random.shuffle(X)
        batch_X = X[:min(mini_batch, len(X))]

        gradient, loss = calculate_gradient(batch_X, weights, activation=activation, logits=logits)
        if show_progress_bar:
            progress_bar.set_description("Current loss: {:.7f}".format(loss))
        for i in range(len(gradient)):
            weights[i] += gradient[i] * lr
    return weights


def Adam(X, weights, activation="ReLU", lr=1e-3, b1=0.9, b2=0.999, epsilon=1e-8, mini_batch=500, epochs=500, logits=True, show_progress_bar=True, descent=True):
    if show_progress_bar:
        progress_bar = trange(epochs)
    else:
        progress_bar = range(epochs)
    for _ in progress_bar:
        random.shuffle(X)
        batch_X = X[:min(mini_batch, len(X))]

        gradient, loss = calculate_gradient(batch_X, weights, activation=activation, logits=logits)

        if show_progress_bar:
            progress_bar.set_description("Current loss: {:.7f}".format(loss))
        m = [[] for _ in range(len(gradient))]
        v = [[] for _ in range(len(gradient))]
        for i, layer in enumerate(gradient):
            if len(m[i]) == 0:
                m[i] = np.zeros_like(layer)
                v[i] = np.zeros_like(layer)
            m[i] = b1 * m[i] + (1 - b1) * layer
            v[i] = b2 * v[i] + (1 - b2) * (layer ** 2)
            M = m[i] / (1 - b1 ** (i + 1))
            V = v[i] / (1 - b2 ** (i + 1))
            if descent:
                weights[i] += ((lr*M)/((V**0.5)+epsilon))
            else:
                weights[i] -= ((lr * M) / ((V ** 0.5) + epsilon))

    return weights