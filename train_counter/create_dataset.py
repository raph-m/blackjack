import numpy as np
import pandas as pd
from multiprocessing import Pool

from environment.dealer import Dealer
from strategies.counters import CountAllCards
from strategies.naive_strategy import simple_play_2


def generate_dataset(n, seed=0, number_of_decks=2, shuffle_every=80):
    dealer = Dealer(counter=CountAllCards(), seed=seed, number_of_decks=number_of_decks, shuffle_every=shuffle_every)
    dataset = np.zeros((n, 17))
    for i in range(n):
        dealer.shuffle_if_needed()
        rc = dealer.deck.counter.get_rc()

        for j in range(1, 14):
            dataset[i, j] = rc[j]
        r, p_blackjacks, d_blackjack, d_burst = simple_play_2(dealer, strategy={"name": "basic"})

        dataset[i, 13] = r
        dataset[i, 14] = p_blackjacks
        dataset[i, 15] = d_blackjack
        dataset[i, 16] = d_burst

    return dataset


def generate_dataset_parallel(n, n_processes=None, id='', number_of_decks=2, shuffle_every=80):
    if n_processes:
        pool = Pool(n_processes)
    else:
        pool = Pool()
    print("N processes: "+str(pool._processes))
    tasks = []
    n_tasks = 50

    seeds = range(n_tasks)
    for i in range(n_tasks):
        kwds = {
            "seed": seeds[i],
            "n": int(n/n_tasks),
            "number_of_decks": number_of_decks,
            "shuffle_every": shuffle_every
        }
        tasks.append(pool.apply_async(generate_dataset, kwds=kwds))
    pool.close()
    pool.join()

    names = [str(i) for i in range(1, 14)]
    names += ["reward", "player_blackjack", "dealer_blackjack", "dealer_burst"]
    data = pd.DataFrame(columns=names)

    for i in range(n_tasks):
        current_data = pd.DataFrame(tasks[i].get(), columns=names)
        data = pd.concat([data, current_data])

    data.to_csv("data/dataset_"+str(n)+".csv")
