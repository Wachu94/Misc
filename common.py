import numpy as np

def calculate_gradient(X, weights, activation="ReLU", logits=True):
    neuron_values = []
    output = X
    for i in range(len(weights)):
        neuron_values.append(np.array(output))
        output = np.dot(output, weights[i])
        if i < len(weights) - 1:
            output = activate(output, activation)
    if logits:
        output = activate(output, "Sigmoid")
    errors = [X - output]
    loss = np.sum(np.sum((errors[len(errors) - 1]) ** 2))
    for i in range(len(weights) - 1):
        errors.append(errors[i].dot(weights[len(weights) - 1 - i].T))
        errors[i + 1] *= neuron_values[len(neuron_values) - 1 - i]
        if activation == "Sigmoid":
            errors[i+1] = errors[i + 1] * (1 - errors[i + 1])
    errors.reverse()

    gradient = []
    for i in range(len(neuron_values)):
        gradient.append(neuron_values[i].T.dot(errors[i]) / neuron_values[i].shape[0])

    return gradient, loss


def setup_weights(layers, minimum=-1, maximum=1):
    weights = []
    for i in range(len(layers) - 1):
        weights.append(np.random.uniform(minimum, maximum, size=(layers[i], layers[i + 1])))
    return weights


def activate(X, func_name):
   if func_name == "ReLU":
       X[X<0] = 0
   elif func_name == "ELU":
       X[X < 0] = np.exp(X[X<0] - 1)
   elif func_name == "Sigmoid":
       for i in range(len(X)):
           X[i] = 1/(1 + np.exp(-X[i]))
   elif func_name == "Softmax":
       sum = 0
       for i in range(len(X)):
           X[i] = np.exp(X[i])
           sum += X[i]
       X /= sum
   return X


def forward_prop(X, weights, activation="ReLU"):
    for i, weight in enumerate(weights):
        X = np.dot(X, weight)
        if i != len(weights) - 1:
            activate(X, activation)
    return X