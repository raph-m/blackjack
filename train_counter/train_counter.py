import random
from train_counter.counter import loss
import numpy as np


def update_weights(x, y, w, b):
    good = False
    x1, x2 = random.sample(range(1, 14), 2)
    while not good:
        good = True
        x1, x2 = random.sample(range(1, 14), 2)
        if w[x1] == w[x2]:
            if w[x1] in [-1, 1]:
                good = False

    if w[x1] == w[x2] or w[x1] == - w[x2]:  # this means w[x1] = 0
        w_0 = w.copy()
        w_0[x1] = 0
        w_0[x2] = 0

        score_0 = loss(x, y, w, b)

        w_1 = w.copy()
        w_1[x1] = -1
        w_1[x2] = 1

        score_1 = loss(x, y, w_1, b)

        w_2 = w.copy()
        w_2[x1] = 1
        w_2[x2] = -1

        score_2 = loss(x, y, w_2, b)

        if score_0 > score_1 and score_0 > score_2:
            return w
        if score_1 >= score_2:
            return score_1
        return score_2

    w_1 = w.copy()
    w_1[x1] = w[x2]
    w_1[x2] = w[x1]

    score_1 = loss(x, y, w_1, b)
    current_score = loss(x, y, w, b)

    if score_1 > current_score:
        return w_1
    return w


def update_bias(x, y, w, b):
    scores = {-1: 0, 0: 0, 1: 0}

    for i in range(-1, 2):
        bp = b + i
        scores[i] = loss(x, y, w, bp)

    best_k = 0
    best_score = 0
    for k, v in scores.items():
        if v < best_score:
            best_k = k

    return b + best_k


def train(df, iterations=50, init="zero"):
    x_cols = [str(i) for i in range(1, 14)]
    x = df[x_cols].values
    y = df["reward"].values
    w = []

    w_thorp = [-1] + [1] * 5 + [0] * 3 + [-1] * 4
    b_thorp = 15

    if init == "random":
        for i in range(4):
            w += random.sample([1, -1, 0], 3)
        w.append(0)

    if init == "zero":
        w = [0] * 13
    w = np.array(w).astype(np.int8)
    b = 0

    for i in range(iterations):
        print("\niteration "+str(i)+": ")
        print("loss: "+str(loss(x, y, w, b)))
        print("w: ")
        print(w)
        print("b: "+str(b))
        w = update_weights(x, y, w, b)
        b = update_bias(x, y, w, b)

    print("\nthorp loss is: "+str(loss(x, y, w_thorp, b_thorp)))
    print("\nthis model loss is: "+str(loss(x, y, w, b)))

    return w, b