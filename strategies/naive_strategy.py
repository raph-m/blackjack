from environment.dealer import Dealer
from util.tools import get_score
import numpy as np
import matplotlib.pyplot as plt
from strategies.counters import ThorpCounter


def my_basic_strategy(hand, dealer_hand, strategy):
    # TODO
    return naive_strategy(hand, dealer_hand, {"name": "naive", "k": 16})


def basic_strategy(hand, dealer_hand, strategy):
    # TODO
    return naive_strategy(hand, dealer_hand, {"name": "naive", "k": 16})


def naive_strategy(hand, dealer_hand, strategy):
    if get_score(hand) > strategy["k"]:
        return "stick"
    return "hit"


def choose_action(hand, dealer_hand, strategy):
    if strategy["name"] == "hit":
        return "hit"
    if strategy["name"] == "naive":
        return naive_strategy(hand, dealer_hand, strategy)
    if strategy["name"] == "basic":
        return basic_strategy(hand, dealer_hand, strategy)
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
        action = choose_action(hand, dealer_cards, strategy=strategy)
        res = dealer.step(action)
    rewards = res["rewards"][0]
    return np.mean(rewards)


def expectancy(strategy, n):
    """
    :param strategy: (dict) la stratégie à tester
    :param n: (int) nombre d'essais
    :return: (float) l'espérance de cette stratégie
    """
    dealer = Dealer()
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

plot_counter(1000000)
