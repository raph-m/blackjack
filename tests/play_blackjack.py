from environment.dealer import Dealer
from util.tools import get_score

action_space = ["hit", "stick", "double", "split"]

dealer = Dealer()

my_money = 10
while True:
    print("\nNew game:")
    print("my money: "+str(my_money))
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
