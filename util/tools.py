import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

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


def check_encoding():
    assert encoding([1, 1, 1], [8]) == "soft.13.8"
    assert encoding([10, 1, 1], [12]) == "hard.12.10"
    assert encoding([13, 12, 1], [1]) == "hard.21.1"
    assert encoding([13, 8, 1], [1]) == "hard.19.1"
    assert encoding([13, 11], [1]) == "pair.10.1"
    assert encoding([7, 7], [1]) == "pair.7.1"

def visualizePolicy(policy):
    #x, y, z_usable_ace, z_no_usable_ac = [], [], [], []
    #s1, s2, ace, actions = Q.shape
    pair, soft, hard = np.zeros((10,10)), np.zeros((10,10)), np.zeros((18,10))
    actions_space={"hit" : 1, "stick" : 2, "double" : 3, "split" : 4}
    for state in policy :
        encoded = state.split(".")
        typ, player, dealer = encoded[0], int(encoded[1]), int(encoded[2])
        if typ == "pair" :
            pair[player-1, dealer-1] = actions_space[policy[state]]
        elif typ == "soft" :
            soft[player-13, dealer-1] = actions_space[policy[state]]
        elif typ == "hard" :
            hard[player-4, dealer-1] = actions_space[policy[state]]

    plt.matshow(pair)
    plt.xlabel("dealer card")
    plt.ylabel("player hand")
    plt.title("base strategy with pairs \n hit : violet, stick : blue, double : green, split : yellow")

    plt.show()
"""
    ax = fig.add_subplot(1,2,1,projection='3d')
    ax.plot_trisurf(x, x, pair, cmap=cm.jet)
    ax.set_xlabel('Dealer card', fontsize=20)
    ax.set_ylabel('Player sum', fontsize=20)
    ax.set_zlabel('State-Value', fontsize=20)
    ax.set_title('No Usable Ace', fontsize=20)
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=15)
    ax.tick_params(axis='z', labelsize=15)
"""



"""
    for i in range(11,s1):
        for j in range(s2):
            y.append(i+1)
            x.append(j+1)
            z_usable_ace.append(np.max(Q[i,j,1,:]))
            z_no_usable_ace.append(np.max(Q[i,j,0,:]))
"""

"""
    ax = fig.add_subplot(1,2,2,projection='3d')
    ax.plot_trisurf(x, y, z_usable_ace, cmap=cm.jet)
    ax.set_xlabel('Dealer card', fontsize=20)
    ax.set_ylabel('Player sum', fontsize=20)
    ax.set_zlabel('State-Value', fontsize=20)
    ax.set_title('Usable Ace', fontsize=20)
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=15)
    ax.tick_params(axis='z', labelsize=15)
"""
