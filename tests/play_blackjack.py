import os
cwd = os.getcwd()
print(cwd)

from environment.dealer import Dealer
from util.tools import get_score

action_space = ["hit", "stick", "double", "split"]

dealer = Dealer(seed=420)


def play(n):
    """
    une fonction pour faire n parties de blackjack
    """
    for i in range(n):
        print("\nNew game:")
        res = dealer.reset()
        while not res["done"]:
            print(res)
            player_playing = res["player_playing"]
            hand_playing = res["hand_playing"]
            hand = res["hands"][player_playing][hand_playing]
            score = get_score(hand)
            print("hand playing: "+str(hand))
            print("your score: "+str(score))
            action = ""
            while action not in action_space:
                action = input("please enter an action")
            res = dealer.step(action)
        print(res)


def shuffle(n):
    """
    une fonction pour tester que on mélange bien les cartes de façon différente à chaque fois.
    """
    counter = 0
    for i in range(n):
        res = dealer.reset()
        while not res["done"]:
            player_playing = res["player_playing"]
            hand_playing = res["hand_playing"]
            hand = res["hands"][player_playing][hand_playing]
            score = get_score(hand)
            if counter == 0:
                print(res)
                print("hand playing: "+str(hand))
                print("your score: "+str(score))
            counter += 1
            action = ""
            while action not in action_space:
                action = "hit"
            res = dealer.step(action)

        if res["shuffle"]:
            counter = 0


play(10)
