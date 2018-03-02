from environment.dealer import Dealer
from util.tools import get_score


def hit_strategy(hand, dealer_cards):
    return "hit"

def choose_action()

def simple_play(dealer, strategy):
    """
    une fonction pour faire n parties de blackjack
    """
    res = dealer.reset()
    while not res["done"]:
        player_playing = res["player_playing"]
        hand_playing = res["hand_playing"]
        dealer_cards = res["dealer_cards"]
        hand = res["hands"][player_playing][hand_playing]
        action = choose_action(hand, dealer_cards)
        action = "hit"
        while action not in action_space:
            action = input("please enter an action")
        res = dealer.step(action)
        print(res)
