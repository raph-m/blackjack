from strategies.naive_strategy import parallel_evaluate_counting_strategy
import json


def compare_high_low_counters():
    n = int(1e6)
    strategy = {"name": "basic"}
    bet_ratio = 30

    print("evaluating High Low counter for n = "+str(n) + " and bet ratio = "+str(bet_ratio))

    for decks in [2, 3, 4, 6]:
        with open("temp_results/nb_events"+str(decks)+"decks.json") as fp:
            nb_events = json.load(fp)
        with open("temp_results/rewards"+str(decks)+"decks.json") as fp:
            rewards = json.load(fp)
        with open("temp_results/params"+str(decks)+"decks.json") as fp:
            params = json.load(fp)

        bet_mapping = {}
        for i in range(-50, 50):
            try:
                bet_mapping[i] = 1 if rewards[i] >= 0 else 0
            except:
                bet_mapping[i] = 1 if i >= 0 else 0

        r0 = parallel_evaluate_counting_strategy(
            strategy,
            n,
            bet_mapping,
            number_of_decks=params["number_of_decks"],
            shuffle_every=params["shuffle_every"],
            bet_ratio=1,
            number_of_players=1
        )

        r1 = parallel_evaluate_counting_strategy(
            strategy,
            n,
            bet_mapping,
            number_of_decks=params["number_of_decks"],
            shuffle_every=params["shuffle_every"],
            bet_ratio=30,
            number_of_players=1
        )

        print("\nnumber of decks: "+str(params["number_of_decks"]))
        print("shuffle every: "+str(params["shuffle_every"]))
        print("with no bet ratio, total reward is: "+str(r0))
        print("with bet ratio, total reward is: "+str(r1))
        print()

