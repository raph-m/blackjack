from strategies.naive_strategy import parallel_evaluate_counting_strategy
strategy = {"name": "basic"}
bet_mapping = {}
for i in range(-50, 50):
    bet_mapping[i] = 1 if i >= 5 else 0

print(bet_mapping[5])


def compare_high_low_counters():
    n = 1e6
    print(parallel_evaluate_counting_strategy(
        strategy,
        n,
        bet_mapping,
        number_of_decks=3,
        shuffle_every=104,
        bet_ratio=1,
        number_of_players=1
    ))
