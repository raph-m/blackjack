from environment.dealer import Dealer
from util.tools import get_score
import numpy as np
import matplotlib.pyplot as plt
from strategies.counters import ThorpCounter
from util.tools import encoding

stick = "stick"
split = "split"
hit = "hit"
double = "double"


def my_basic_strategy(hand, dealer_hand, strategy):
    # TODO
    return naive_strategy(hand, dealer_hand, {"name": "naive", "k": 16})


def basic_strategy(hand, dealer_hand, strategy, can_split=True):
    encoded = encoding(hand, dealer_hand, can_split=can_split).split(".")
    type, player, dealer = encoded[0], int(encoded[1]), int(encoded[2])

    if player in [21, 22]:
        return stick
    
    if type == "pair":
        if player in [1, 8]:
            return split
        if player == 10:
            return stick
        if player == 9:
            if dealer in [7, 10, 1]:
                return stick
            else:
                return split
        if player == 7:
            if dealer in [8, 9, 10, 1]:
                return hit
            else:
                return split
        if player == 6:
            if dealer in [7, 8, 9, 10, 1]:
                return hit
            else:
                return split
        if player == 5:
            if dealer in [10, 1]:
                return hit
            else:
                return double
        if player == 4:
            if dealer in [5, 6]:
                return split
            else:
                return hit
        if player in [2, 3]:
            if dealer in [8, 9, 10, 1]:
                return hit
            else:
                return split

    if type == "soft":
        if player == 20:
            return stick
        if player == 19:
            if dealer == 6:
                return double
            else:
                return stick
        if player == 18:
            if dealer in [2, 3, 4, 5, 6]:
                return double
            if dealer in [7, 8]:
                return stick
            return hit
        if player == 17:
            if dealer in [3, 4, 5, 6]:
                return double
            return hit
        if player in [16, 15]:
            if dealer in [4, 5, 6]:
                return double
            return hit
        if player in [13, 14]:
            if dealer in [5, 6]:
                return double
            return hit

    if type == "hard":
        if player in [17, 18, 19, 20]:
            return stick
        if player in [13, 14, 15, 16]:
            if dealer in [2, 3, 4, 5, 6]:
                return stick
            return hit
        if player == 12:
            if dealer in [4, 5, 6]:
                return stick
            return hit
        if player == 11:
            return double
        if player == 10:
            if dealer in [10, 1]:
                return hit
            return double
        if player == 9:
            if dealer in [3, 4, 5, 6]:
                return double
            return hit
        if player in [2, 3, 4, 5, 6, 7, 8]:
            return hit
        # normalement c'est ça ça qu'on a dans la stratégie de base mais le fait de pas tj pouvoir splitter
        # ça fout totalement la merde
        # if player in [5, 6, 7, 8]:
        #     return hit


def naive_strategy(hand, dealer_hand, strategy):
    if get_score(hand) > strategy["k"]:
        return "stick"
    return "hit"


def choose_action(hand, dealer_hand, strategy, can_split=True):
    if strategy["name"] == "hit":
        return "hit"
    if strategy["name"] == "naive":
        return naive_strategy(hand, dealer_hand, strategy)
    if strategy["name"] == "basic":
        return basic_strategy(hand, dealer_hand, strategy, can_split=can_split)
    if strategy["name"] == "my_basic":
        return my_basic_strategy(hand, dealer_hand, strategy)


def simple_play(dealer, strategy):
    """
    une fonction pour récupérer le résultat sur une partie de blackjack suivant une stratégie
    """
    res = dealer.reset()
    while not res["done"]:
        player_playing = res["player_playing"]
        hand_playing = res["hand_playing"]
        dealer_cards = res["dealer_cards"]
        hand = res["hands"][player_playing][hand_playing]
        can_split = len(res["hands"][player_playing]) == 1
        action = choose_action(hand, dealer_cards, strategy=strategy, can_split=can_split)
        res = dealer.step(action)
    rewards = res["rewards"][0]
    return np.sum(rewards)


def expectancy(strategy, n):
    """
    :param strategy: (dict) la stratégie à tester
    :param n: (int) nombre d'essais
    :return: (float) l'espérance de cette stratégie
    """
    dealer = Dealer(seed=15)
    total = 0.0
    for i in range(n):
        total += simple_play(dealer, strategy)
    return total / n


def best_naive_strategy(n):
    results = np.zeros(22)
    for k in range(22):
        strat = {"name": "naive", "k": k}
        results[k] = expectancy(strat, n)
        print(str(k)+": "+str(results[k]*100))
    plt.plot(range(22), results*100)
    plt.show()


def plot_counter(n):

    dealer = Dealer(counter=ThorpCounter())

    nb_events = {}
    rewards = {}

    for i in range(n):
        dealer.reset()
        for j in range(50):
            dealer.deck.next_card()

        r = simple_play(dealer, strategy={"name": "basic"})
        count = dealer.deck.counter.get_rc()
        try:
            nb_events[count] += 1
            rewards[count] += r
        except:
            nb_events[count] = 1
            rewards[count] = r

    print(nb_events)

    for k, v in nb_events.items():
        rewards[k] /= nb_events[k]

    ks = []
    vs = []
    for k, v in rewards.items():
        ks.append(k)
        vs.append(v)

    plt.scatter(ks, vs)
    plt.show()

# print(expectancy({"name": "basic"}, 1000000))
best_naive_strategy(1000000)
