from environment.dealer import Dealer
from util.tools import get_score
from strategies.counters import ThorpCounter

action_space = ["hit", "stick", "double", "split"]
number_of_players = 1
number_of_decks = 4
shuffle_every = 52
seed = 1
counter = ThorpCounter()


dealer = Dealer(
    number_of_players=number_of_players,
    number_of_decks=number_of_decks,
    shuffle_every=shuffle_every,
    seed=seed,
    counter=counter
)


def play(n):
    """
    play n games of blackjack
    """
    for i in range(n):
        print("\nNew game:")
        res = dealer.reset()
        while not res["done"]:
            print("hands:")
            print(res["hands"])
            print("dealer:")
            print(res["dealer_cards"])
            player_playing = res["player_playing"]
            hand_playing = res["hand_playing"]
            hand = res["hands"][player_playing][hand_playing]
            score = get_score(hand)
            print("hand playing: "+str(hand))
            print("your score: "+str(score))
            action = ""
            while action not in action_space:
                action = input("please enter an action\n")
            res = dealer.step(action)
        print(res)

play(10)
