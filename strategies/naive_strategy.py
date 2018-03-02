from environment.dealer import Dealer
from util.tools import get_score
import numpy as np
import matplotlib.pyplot as plt


def naive_strategy(hand, dealer_hand, strategy):
    if get_score(hand) > strategy["k"]:
        return "stick"
    return "hit"


def choose_action(hand, dealer_hand, strategy):
    if strategy["name"] == "hit":
        return "hit"
    if strategy["name"] == "naive":
        return naive_strategy(hand, dealer_hand, strategy)


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

# best_naive_strategy(10000)
