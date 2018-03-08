import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import pandas as pd


def get_value(cards):
    """
    :param cards: (list of ints) the cards to evaluate
    :return: value (int) the value of the cards where we count aces as one point.
    """
    value = 0

    for i in range(len(cards)):
        if cards[i] < 11:
            value += cards[i]
        else:
            value += 10

    return value


def get_values(cards):
    """
    :param cards: (list of ints) the cards to evaluate
    :return: values (list of ints) the possible values of the set of cards where an ace can count as one point
    or eleven points
    """
    values = [get_value(cards)]
    for i in range(len(cards)):
        if cards[i] < 2:
            current = []
            for p in values:
                current.append(p+10)
            for c in current:
                values.append(c)
    return values


def get_score(cards):
    """
    :param cards: (list of ints) the cards to evaluate
    :return: score (int) the best possible score of the set of cards. 22 is blackjack and 0 means that the
    player burst.
    """

    max_score = 0
    min_score = 30

    for v in get_values(cards):
        if 22 > v > max_score:
            max_score = v
        if v < min_score:
            min_score = v

    if min_score > 21:
        return 0

    if max_score == 21 and len(cards) < 3:
        return 22

    return max_score


def encoding(player, dealer, can_split=True):
    dealer_encoding = str(get_value(dealer))

    if len(player) == 2 and can_split:
        if player[0] == player[1] or (player[0] >= 10 and player[1] >= 10):
            value = min(10, player[0])
            return "pair."+str(value)+"."+dealer_encoding

    player_score = get_score(player)
    if get_value(player) == player_score:
        return "hard."+str(player_score)+"."+dealer_encoding

    return "soft."+str(player_score)+"."+dealer_encoding


def is_soft_17(cards):
    if get_score(cards) == 17:
        if get_value(cards) < get_score(cards):
            return True
    return False


def check_encoding():
    assert encoding([1, 1, 1], [8]) == "soft.13.8"
    assert encoding([10, 1, 1], [12]) == "hard.12.10"
    assert encoding([13, 12, 1], [1]) == "hard.21.1"
    assert encoding([13, 8, 1], [1]) == "hard.19.1"
    assert encoding([13, 11], [1]) == "pair.10.1"
    assert encoding([7, 7], [1]) == "pair.7.1"


def visualizePolicy(policy, id):
    pair, soft, hard = np.zeros((10, 10)), np.zeros((8, 10)), np.zeros((17, 10))
    actions_space = {"hit": 1, "stick": 2, "double": 3, "split": 4}
    pol = dict(policy)
    if "epochs" in pol :
        del pol["epochs"]
    if "name" in pol :
        del pol["name"]
    for state in pol :
        encoded = state.split(".")
        typ, player, dealer = encoded[0], int(encoded[1]), int(encoded[2])
        if typ == "pair":
            pair[10-player, dealer-1] = actions_space[policy[state]]
        elif typ == "soft" and player < 21:
            soft[20-player, dealer-1] = actions_space[policy[state]]
        elif typ == "hard" and 3 < player < 21:
            hard[20-player, dealer-1] = actions_space[policy[state]]

    rpAs = pair[-1, :].reshape(1, 10)
    pair = np.r_[rpAs, pair]
    pair = np.delete(pair, -1, axis=0)
    cpAs = pair[:, 0].reshape(10, 1)
    pair = np.append(pair, cpAs, axis=1)
    pair = np.delete(pair, 0, axis=1)

    csAs = soft[:, 0].reshape(8, 1)
    soft = np.append(soft, csAs, axis=1)
    soft = np.delete(soft, 0, axis=1)

    chAs = hard[:, 0].reshape(17, 1)
    hard = np.append(hard, chAs, axis=1)
    hard = np.delete(hard, 0, axis=1)

    x = np.arange(10)
    ys = np.arange(8)
    yh = np.arange(17)
    dlabel = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "As"]
    plabel = ["As,As", "10,10","9,9", "8,8", "7,7", "6,6", "5,5", "4,4", "3,3", "2,2"]
    slabel = ["A,9", "A,8", "A,7", "A,6", "A,5", "A,4", "A,3", "A,2"]
    hlabel = ["20", "19", "18", "17", "16", "15", "14", "13", "12", "11", "10", "9", "8", "7", "6", "5", "4"]
    plt.matshow(pair)
    plt.xlabel("dealer card")
    plt.ylabel("player hand")
    plt.title("base strategy with pairs \n violet : hit, blue : stick, green :" + "double, yellow : split")
    plt.xticks(x, dlabel)
    plt.yticks(x, plabel)
    plt.savefig("results/base_pair_"+str(id)+".png")
    plt.close()

    plt.matshow(soft)
    plt.xlabel("dealer card")
    plt.ylabel("player hand")
    plt.title("base strategy with soft hands \n violet : hit, blue : stick, " + "yellow : double")
    plt.xticks(x, dlabel)
    plt.yticks(ys, slabel)
    plt.savefig("results/base_soft_"+str(id)+".png")
    plt.close()

    plt.matshow(hard)
    plt.xlabel("dealer card")
    plt.ylabel("player hand")
    plt.title("base strategy with hard hands \n violet : hit, blue : stick, " + "yellow : double")
    plt.xticks(x, dlabel)
    plt.yticks(yh, hlabel)
    plt.savefig("results/base_hard_"+str(id)+".png")
    plt.close()

def change_datatype(df, int_cols=None):
    if not int_cols:
        int_cols = list(df.select_dtypes(include=['int']).columns)
    for col in int_cols:
        if np.max(df[col]) <= 127 and np.min(df[col]) >= -128:
            df[col] = df[col].astype(np.int8)
        elif np.max(df[col]) <= 32767 and np.min(df[col]) >= -32768:
            df[col] = df[col].astype(np.int16)
        elif np.max(df[col]) <= 2147483647 and np.min(df[col]) >= -2147483648:
            df[col] = df[col].astype(np.int32)
        else:
            df[col] = df[col].astype(np.int64)


def change_datatype_float(df, float_cols=None):
    if not float_cols:
        int_cols = list(df.select_dtypes(include=['int']).columns)
    float_cols = list(df.select_dtypes(include=['float']).columns)
    for col in float_cols:
        df[col] = df[col].astype(np.float32)


def memory_usage(df):
    mem = df.memory_usage(index=True).sum()
    return mem / 1024**2, " MB"
