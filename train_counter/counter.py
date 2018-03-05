import numpy as np


def loss(x, y, w, b):
    pred = (np.dot(x, np.transpose(w)) - b) >= 0
    print("shape of w: " + str(pred.shape))
    print("shape of pred: " + str(pred.shape))
    print("shape of y: " + str(y.shape))
    b = (pred > 0)

    a = (pred > 0) * (y > 1) * y * 100
    print("(pred > 0) * (y > 1) * y * 100: "+str(a.shape))

    return np.mean((pred-y)**2 - (pred > 0) * (y > 1) * y * 100)