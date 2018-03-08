import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool
import json

from environment.dealer import Dealer
from util.tools import get_score, encoding
from strategies.counters import ThorpCounter


stick = "stick"
split = "split"
hit = "hit"
double = "double"


def my_basic_strategy(hand, dealer_hand, strategy, can_split=True):
    state = encoding(hand, dealer_hand, can_split)
    return strategy[state]


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


def save_base_policy():
    policy = {}
    for i in range(1, 11):
        for j in range(1, 11):
            player = [i]
            dealer = [j]
            state = encoding(player, dealer, can_split=True)
            enc = state.split(".")
            if int(enc[1]) != 0:
                policy[state] = basic_strategy(player, dealer, None, True)
    for i in range(1, 11):
        for j in range(1, 11):
            for k in range(1, 11):
                player = [i, j]
                dealer = [k]
                state = encoding(player, dealer, can_split=True)
                enc = state.split(".")
                if int(enc[1]) != 0:
                    policy[state] = basic_strategy(player, dealer, None, True)
    for i in range(1, 11):
        for j in range(1, 11):
            for k in range(1, 11):
                for l in range(1, 11):
                    player = [i, j, k]
                    dealer = [l]
                    state = encoding(player, dealer, can_split=True)
                    enc = state.split(".")
                    if int(enc[1]) != 0:
                        policy[state] = basic_strategy(player, dealer, None, True)
    with open("strategy_generator/base_wiki_policy.json", "w") as fp:
        json.dump(policy, fp)


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
        return my_basic_strategy(hand, dealer_hand, strategy, can_split=can_split)


def simple_play(dealer, strategy, mean=True):
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
    if mean:
        return np.mean(rewards)
    return np.sum(rewards)


def simple_play_2(dealer, strategy):
    res = dealer.reset()
    while not res["done"]:

        player_playing = res["player_playing"]
        hand_playing = res["hand_playing"]
        dealer_cards = res["dealer_cards"]
        hand = res["hands"][player_playing][hand_playing]
        can_split = len(res["hands"][player_playing]) == 1

        action = choose_action(hand, dealer_cards, strategy=strategy, can_split=can_split)
        res = dealer.step(action)

    player_blackjacks = [get_score(cards) for cards in res["hands"][0]]
    player_blackjacks = [s == 22 for s in player_blackjacks]
    player_blackjacks = [1 if s else 0 for s in player_blackjacks]
    dealer_blackjack = 1 if get_score(res["dealer_cards"]) == 22 else 0
    dealer_burst = 1 if get_score(res["dealer_cards"]) == 0 else 0
    rewards = res["rewards"][0]

    return np.mean(rewards), np.mean(player_blackjacks), dealer_blackjack, dealer_burst


def expectancy(strategy=None, n=100, seed=300, number_of_decks=2, shuffle_every=52):
    dealer = Dealer(seed=seed, number_of_decks=number_of_decks, shuffle_every=shuffle_every)
    total = 0.0
    for i in range(n):
        total += simple_play(dealer, strategy)
    return total / n


def parallel_expectancy(strategy, n, number_of_decks=2, shuffle_every=52):
    pool = Pool()
    tasks = []
    n_tasks = 50
    results = np.zeros(n_tasks)
    seeds = range(n_tasks)
    for i in range(n_tasks):
        kwds = {
            "strategy": strategy,
            "seed": seeds[i],
            "n": int(n/n_tasks),
            "number_of_decks": number_of_decks,
            "shuffle_every": shuffle_every
        }
        tasks.append(pool.apply_async(expectancy, kwds=kwds))
    pool.close()
    pool.join()
    for i in range(n_tasks):
        results[i] = tasks[i].get()

    return np.mean(results)


def best_naive_strategy(n):
    ks = range(8, 19)
    results = np.zeros(len(ks))
    for i in range(len(ks)):
        strat = {"name": "naive", "k": ks[i]}
        results[i] = parallel_expectancy(strat, n)
        print(str(ks[i])+": "+str(results[i]*100))

    y_error = 100 * np.ones(len(results)) / np.sqrt(n)
    plt.errorbar(ks, results * 100, yerr=[y_error, y_error], fmt='o')
    plt.plot(ks, np.zeros(len(results)), label="zero")
    plt.legend()
    plt.title("hit on k, stick on k+1")
    plt.xlabel("k")
    plt.ylabel("average reward for a 100 dollars initial bet")
    plt.show()


def blackjack_counter(n=100, seed=300):
    dealer = Dealer(counter=ThorpCounter(), seed=seed, blackjack_reward=2)

    nb_events = {}
    rewards = {}
    player_blackjacks = {}
    dealer_blackjacks = {}
    dealer_burst = {}

    for i in range(n):
        dealer.reset()
        for j in range(50):
            dealer.deck.next_card()

        count = dealer.deck.counter.get_rc()
        r, p_blackjacks, d_blackjack, d_burst = simple_play_2(dealer, strategy={"name": "basic"})

        try:
            nb_events[count] += 1
            rewards[count] += r
            player_blackjacks[count] += p_blackjacks
            dealer_blackjacks[count] += d_blackjack
            dealer_burst[count] += d_burst

        except:
            nb_events[count] = 1
            rewards[count] = r
            player_blackjacks[count] = p_blackjacks
            dealer_blackjacks[count] = d_blackjack
            dealer_burst[count] = d_burst

    return nb_events, rewards, dealer_blackjacks, player_blackjacks, dealer_burst


def plot_counter(n=100, seed=300, number_of_decks=3, shuffle_every=104, counter=ThorpCounter()):

    dealer = Dealer(number_of_decks=number_of_decks, shuffle_every=shuffle_every, counter=counter, seed=seed)

    nb_events = {}
    rewards = {}
    done = False
    counts_to_compute = range(-12, 12)

    for i in counts_to_compute:
        nb_events[i] = 0
        rewards[i] = 0

    while not done:
        dealer.deck.next_card()
        dealer.shuffle_if_needed()
        count = dealer.deck.counter.get_rc()

        if count in counts_to_compute:
            if nb_events[count] < n:

                r = simple_play(dealer, strategy={"name": "basic"})
                nb_events[count] += 1
                rewards[count] += r

                done = True
                for i in counts_to_compute:
                    if nb_events[i] < n:
                        done = False
                if done:
                    break
                else:
                    continue

    return nb_events, rewards


def plot_counter_parallel(
        n, show=True,
        n_processes=None,
        id='',
        number_of_decks=3,
        shuffle_every=104,
        counter=ThorpCounter()
):
    if n_processes:
        pool = Pool(n_processes)
    else:
        pool = Pool()

    tasks = []
    n_tasks = 50

    seeds = range(n_tasks)
    for i in range(n_tasks):
        kwds = {
            "seed": seeds[i],
            "n": int(n/n_tasks),
            "number_of_decks": number_of_decks,
            "shuffle_every": shuffle_every,
            "counter": counter
        }
        tasks.append(pool.apply_async(plot_counter, kwds=kwds))
    pool.close()
    pool.join()
    nb_events = {}
    rewards = {}
    for i in range(n_tasks):
        current_nb_events, current_rewards = tasks[i].get()

        for k, v in current_nb_events.items():
            try:
                nb_events[k] += current_nb_events[k]
                rewards[k] += current_rewards[k]
            except:
                nb_events[k] = current_nb_events[k]
                rewards[k] = current_rewards[k]

    for k, v in nb_events.items():
        rewards[k] /= nb_events[k]

    ks = []
    vs = []
    for k, v in rewards.items():
        ks.append(k)
        vs.append(v)

    if show:
        plt.scatter(ks, vs)
        plt.show()

    else:
        print(nb_events)
        print(rewards)
        with open("temp_results/nb_events"+id+".json", "w") as fp:
            json.dump(nb_events, fp)
        with open("temp_results/rewards"+id+".json", "w") as fp:
            json.dump(rewards, fp)
        with open("temp_results/params"+id+".json", "w") as fp:
            json.dump({"number_of_decks": number_of_decks, "shuffle_every": shuffle_every}, fp)

        print("saved results in temp_results")

def evaluate_counting_strategy(
        n=1000,
        strategy=None,
        bet_mapping=None,
        seed=1,
        number_of_decks=3,
        shuffle_every=104,
        bet_ratio=200,
        number_of_players=5,
        counter=ThorpCounter()
):
    dealer = Dealer(
        number_of_decks=number_of_decks,
        shuffle_every=shuffle_every,
        seed=seed,
        number_of_players=number_of_players,
        counter=counter
    )
    total = 0.0
    for i in range(n):
        dealer.shuffle_if_needed()
        count = dealer.deck.counter.get_rc()
        total += simple_play(dealer, strategy, mean=False) * (1 + bet_mapping[count] * (bet_ratio - 1))
    return total


def parallel_evaluate_counting_strategy(
        strategy,
        n,
        bet_mapping,
        number_of_decks=3,
        shuffle_every=104,
        bet_ratio=200,
        number_of_players=5,
        counter=ThorpCounter()
):
    pool = Pool()
    print("N processes: "+str(pool._processes))
    tasks = []
    n_tasks = 50
    results = np.zeros(n_tasks)
    seeds = range(n_tasks)
    for i in range(n_tasks):
        kwds = {
            "strategy": strategy,
            "seed": seeds[i],
            "n": int(n/n_tasks),
            "number_of_decks": number_of_decks,
            "shuffle_every": shuffle_every,
            "bet_ratio": bet_ratio,
            "bet_mapping": bet_mapping,
            "number_of_players": number_of_players,
            "counter": counter
        }
        tasks.append(pool.apply_async(evaluate_counting_strategy, kwds=kwds))
    pool.close()
    pool.join()
    for i in range(n_tasks):
        results[i] = tasks[i].get()

    return np.sum(results)


def read_counter_results(id='', get_baseline=False, baseline=None):
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
        if nb_events[k] > 10:
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
    plt.plot(ks, ks * 0, label="zero")
    title_str = "number of decks: "+str(params["number_of_decks"])+", shuffle every: "+str(params["shuffle_every"])
    plt.title(title_str)
    plt.xlabel("counter")
    plt.ylabel("average reward")

    if get_baseline:
        n = int(1e6)
        baseline = parallel_expectancy(
            {"name": "basic"},
            n,
            number_of_decks=params["number_of_decks"],
            shuffle_every=params["shuffle_every"]
        )
        plt.plot(ks, np.ones(len(ks)) * baseline, label="avg reward = "+str(baseline))

    if baseline:
        plt.plot(ks, np.ones(len(ks)) * baseline, label="avg reward = "+str(baseline))

    plt.legend()
    print("saving graph in results")
    plt.savefig("results/" + id + ".png")
