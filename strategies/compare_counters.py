from strategies.strategies import parallel_evaluate_counting_strategy
import json
from strategies.counters import PersonalizedCounter, hi_opt_1, hi_opt_2, omega_2, ko, default_thorp, my_counter0, my_counter1
import numpy as np
import matplotlib.pyplot as plt


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


def compare_counters(n, number_of_decks, shuffle_every):
    strategy = {"name": "basic"}

    print("evaluating different counters for n = " + str(n))
    print("number of decks: " + str(number_of_decks))
    print("shuffle every: " + str(shuffle_every))

    ws = []
    names = []
    bs = []
    if number_of_decks == 4 and shuffle_every == 52:
        ws.append(my_counter0)
        ws.append(my_counter1)
        names.append("my_3_level_counter_with_b=6")
        names.append("my_5_level_counter_with_b=6")
        bs.append(6)
        bs.append(6)
        ws.append(my_counter0)
        ws.append(my_counter1)
        names.append("my_3_level_counter_with_b=7")
        names.append("my_5_level_counter_with_b=7")
        bs.append(7)
        bs.append(7)

        famous_counters = [default_thorp, hi_opt_1, hi_opt_2, ko, omega_2]
        famous_counters_names = ["default_thorp", "hi_opt_1", "hi_opt_2", "ko", "omega_2"]
        ws += famous_counters
        names += famous_counters_names
        bs += [0] * len(famous_counters_names)

    bet_mapping = {}
    for j in range(-50, 50):
        bet_mapping[j] = 1 if j >= 0 else 0

    baseline = parallel_evaluate_counting_strategy(
        strategy,
        n,
        bet_mapping,
        number_of_decks=number_of_decks,
        shuffle_every=shuffle_every,
        bet_ratio=1,
        number_of_players=1,
        counter=PersonalizedCounter(hi_opt_1)
    )

    print("baseline is " + str(baseline))

    for bet_ratio in [10, 30, 100, 1000]:
        print("bet ratio is now :"+str(bet_ratio))
        for i in range(len(names)):
            if names[i] in famous_counters_names:
                with open("temp_results/rewards" + names[i] + ".json") as fp:
                    rewards = json.load(fp)

                bet_mapping = {}
                for j in range(-50, 50):
                    try:
                        bet_mapping[j] = 1 if rewards[str(j)] >= 0 else 0
                    except:
                        bet_mapping[j] = 1 if j >= 0 else 0
            else:
                bet_mapping = {}
                for j in range(-50, 50):
                    bet_mapping[j] = 1 if j >= bs[i] else 0

            r1 = parallel_evaluate_counting_strategy(
                strategy,
                n,
                bet_mapping,
                number_of_decks=number_of_decks,
                shuffle_every=shuffle_every,
                bet_ratio=bet_ratio,
                number_of_players=1,
                counter=PersonalizedCounter(ws[i])
            )

            print("computing for counter: " + names[i])
            print("with bet ratio = " + str(bet_ratio) + ", total reward is: " + str(r1))
            print()


def plot_counter_results(id=''):
    with open("temp_results/nb_events"+id+".json", "r") as fp:
        nb_events = json.load(fp)
    with open("temp_results/rewards"+id+".json", "r") as fp:
        rewards = json.load(fp)
    with open("temp_results/params"+id+".json", "r") as fp:
        params = json.load(fp)

    print(nb_events)
    print(rewards)
    ks = []
    vs = []
    y_error = []
    for k, v in rewards.items():
        if nb_events[k] > 1000:
            ks.append(k)
            vs.append(v)
            y_error.append(nb_events[k])

    ks = np.array(ks).astype(int)
    vs = np.array(vs)
    y_error = np.array(y_error)
    y_error = 1 / np.sqrt(y_error)

    order = np.argsort(ks)
    ks = ks[order]
    vs = vs[order]

    plt.errorbar(ks, vs, yerr=[y_error, y_error], fmt='o')
    plt.plot(ks, ks * 0)
    plt.title("number of decks: "+str(params["number_of_decks"])+", shuffle every: "+str(params["shuffle_every"])+", counter = "+id)
    plt.xlabel("counter")
    plt.ylabel("average reward")
    plt.show()
