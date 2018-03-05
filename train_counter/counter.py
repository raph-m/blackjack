import numpy as np


def loss(x, y, w, b):
    pred = (np.dot(x, np.transpose(w)) - b) >= 0
    return np.mean((pred-y)**2 - (pred > 0) * (y > 1) * y * 100)
