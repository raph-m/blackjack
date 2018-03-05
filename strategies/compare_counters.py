from strategies.naive_strategy import parallel_evaluate_counting_strategy
import json
from strategies.counters import PersonalizedCounter, hi_opt_1, hi_opt_2, omega_2, ko, default_thorp


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


def compare_counters(number_of_decks, shuffle_every):
    n = int(1e6)
    strategy = {"name": "basic"}
    bet_ratio = 30

    print("evaluating different counters for n = " + str(n) + " and bet ratio = " + str(bet_ratio))
    print("number of decks: " + str(number_of_decks))
    print("shuffle every: " + str(shuffle_every))

    ws = []
    names = []
    bs = []
    if number_of_decks == 4 and shuffle_every == 52:
        ws.append({1: 0, 2: 0, 3: 1, 4: 1, 5: 2, 6: 1, 7: 0, 8: 0, 9: -1, 10: -2, 11: 0, 12: -1, 13: -1})
        ws.append({1: 0, 2: 0, 3: 0, 4: 1, 5: 1, 6: 0, 7: 0, 8: 0, 9: 0, 10: -1, 11: 0, 12: -1, 13: 0})
        names.append("my 5 level counter with b = 6")
        names.append("my 3 level counter with b = 6")
        bs.append(6)
        bs.append(6)
        ws.append({1: 0, 2: 0, 3: 1, 4: 1, 5: 2, 6: 1, 7: 0, 8: 0, 9: -1, 10: -2, 11: 0, 12: -1, 13: -1})
        ws.append({1: 0, 2: 0, 3: 0, 4: 1, 5: 1, 6: 0, 7: 0, 8: 0, 9: 0, 10: -1, 11: 0, 12: -1, 13: 0})
        names.append("my 5 level counter with b = 7")
        names.append("my 3 level counter with b = 7")
        bs.append(7)
        bs.append(7)

        famous_counters = [default_thorp, hi_opt_1, hi_opt_2, ko, omega_2]
        famous_counters_names = ["default_thorp", "hi_opt_1", "hi_opt_2", "ko", "omega_2"]
        ws += famous_counters
        names += famous_counters_names

        for counter_dic in famous_counters:




    # coefs: [-0.43015842, -0.14951642, 0.75302885, 1.45367159, 1.69597542, 0.71873267, 0.0932644, -0.18514274, -0.77762071, -1.90319907, 0.05352541, -1.38579426, -0.76848075]
    # intercept: -6.93728315673
    # thus we can choose -5 levels- w = {1: 0, 2: 0, 3: 1, 4: 1, 5: 2, 6: 1, 7: 0, 8: 0, 9: -1, 10: -2, 11: 0, 12: -1, 13: -1}
    # or -3 levels- w = {1: 0, 2: 0, 3: 0, 4: 1, 5: 1, 6: 0, 7: 0, 8: 0, 9: 0, 10: -1, 11: 0, 12: -1, 13: 0}
    # for this situation, we can choose a threshold of 6 or 7 (to be decided)

    for decks in [2, 3, 4, 6]:
        with open("temp_results/nb_events" + str(decks) + "decks.json") as fp:
            nb_events = json.load(fp)
        with open("temp_results/rewards" + str(decks) + "decks.json") as fp:
            rewards = json.load(fp)
        with open("temp_results/params" + str(decks) + "decks.json") as fp:
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


        print("with no bet ratio, total reward is: " + str(r0))
        print("with bet ratio, total reward is: " + str(r1))
        print()
