import random
from train_counter.counter import loss
import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn.model_selection import train_test_split
import time
import json

def update_weights(x, y, w, b):
    good = False
    x1, x2 = random.sample(range(1, 14), 2)
    while not good:
        good = True
        x1, x2 = random.sample(range(0, 12), 2)
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
            return w_0
        if score_1 >= score_2:
            return w_1
        return w_2

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

def train_w_ridge(name):
    data = pd.read_csv("data/"+name)
    name = name.split("_")
    n_deck = name[4]
    tmp = name[6].split(".")
    shuffle = tmp[0]
    #print (data.describe())
    x_cols = [str(i) for i in range(1, 14)]
    X = data[x_cols].values
    y = data["reward"].values
    coef = np.zeros(13)
    intercept = 0
    score = 0
    for i in range(1000):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        reg = linear_model.Ridge(alpha=0.5, normalize=True, fit_intercept=True , solver='cholesky')
        #beg = time.time()
        reg.fit(X_train, y_train)
        score += reg.score(X_test, y_test)/10
        coef += reg.coef_
        intercept += reg.intercept_
        #end = time.time()
    print ("mean score:", score)
    print ("mean coefs:", coef)
    print ("mean intercept:", intercept)
    with open("temp_results/res_"+n_deck+"_"+shuffle+".json", "w") as fp:
        json.dump(
        {
            "intercept": str(intercept),
            "coefs": str(coef)
        },
        fp
        )
    #print(end-beg)
