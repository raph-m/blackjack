import json

"""
# generate a policy with a Monte Carlo RL algorithm and store it in a json file
from strategy_generator.base_monte_carlo import MC
policy = MC(epochs=epochs, epsilon=1.0/alpha)
policy["name"] = "my_basic"
policy["epochs"] = epochs
print(policy)
with open("strategy_tuning/"+str(epochs)+"_"+str(alpha)+".json", "w") as fp:
    json.dump(policy, fp)
"""

"""
# generate a policy with a Q learning algorithm
from strategy_generator.base_qlearning import QLearn
epochs = int(1e8)
with open("strategy_tunning/qlearn_hyper_parameters.json", "r") as fp:
    hyp = json.load(fp)
policy = QLearn(epochs=epochs, epsilon=hyp["epsilon"], alpha=hyp["alpha"], gamma=hyp["gamma"])
policy["name"] = "my_basic"
policy["epochs"] = epochs
# we obtain for this policy an expectancy of -1.67%
"""


# Load a strategy designed with n epochs
epochs = 100000000
alpha = 10
with open("strategy_generator/base_qlearn_policy_opt.json", "r") as fp:
    policy = json.load(fp)

print(policy["soft.19.4"])
policy["name"] = "my_basic"


"""
#save wiki base strategy the load it
from strategies.naive_strategy import save_base_policy
#save_base_policy()
with open("strategy_generator/base_wiki_policy.json", "r") as fp:
    policy_2 = json.load(fp)
policy_2["name"] = "my_basic"
policy_2["epochs"] = 1
#print (policy_2)
"""

"""
# Evaluate the policy with parallel computing
from strategies.naive_strategy import parallel_expectancy, expectancy
import time
start = time.time()
n_tries = int(1e6)
print(parallel_expectancy(policy_2, n_tries))
end = time.time()
print("parallel time: ")
print(end-start)
"""


"""
# implement dfo to find the best hyper parameters for MC and Q-learning
from strategy_tuning.dfo_tuning import tune
tune("qlearn")
# results: epsilon = 0.1989, alpha = 0.0362, gamma = 0.9587
tune("MC")
"""

"""
# how to use the card counter:
from environment.dealer import Dealer
from strategies.counters import CountAllCards
from strategies.naive_strategy import simple_play_2

dealer = Dealer(counter=CountAllCards(), seed=0)
total = 0.0
for i in range(10):
    print("new game: ")
    print("number of aces: "+str(dealer.deck.counter.get_rc()[1]))
    print("number of kings: "+str(dealer.deck.counter.get_rc()[13]))

    r, p_blackjacks, d_blackjack, d_burst = simple_play_2(dealer, strategy={"name": "basic"})
    print("reward: "+str(r))
    print("player did a blackjack: "+str(p_blackjacks))
    print("dealer did a blackjack: "+str(d_blackjack))
    print("dealer burst: "+str(d_burst))
    print("")
"""


# Visualize the policy in 3 figures for pairs, soft hands and hard hands
from util.tools import visualizePolicy
visualizePolicy(policy)
#visualizePolicy(policy_2)


"""
#create n play for count learning
import time
n = int(1e6)
from train_counter.create_dataset import generate_dataset_parallel
start = time.time()
generate_dataset_parallel(n, number_of_decks=4, shuffle_every=52)
generate_dataset_parallel(n)
end = time.time()
print(end-start)
"""

"""
from train_counter.train_counter import train_w_ridge
train_w_ridge("dataset_1000000_n_deck_2_shuffle_80.csv")
train_w_ridge("dataset_1000000_n_deck_4_shuffle_52.csv")

# results for 2 decks, shuffle 80
# coefs: [-1.54658578, 1.46565743, 1.64606452, 2.06966632, 2.21852635, 2.25132327, 0.88227194, 0.4281363, -0.85675855, -2.3969003, -1.91884622, -2.27488822, -2.06085728]
# intercept: -5.8449593318
# thus we can choose -uncentered and with 5 levels- w = {1: -2, 2: 1, 3: 2, 4: 2, 5: 2, 6: 2, 7: 1, 8: 0, 9: -1, 10: -2, 11: -2, 12: -2, 13: -2}
# or -centered and with 5 levels- w = {1: -2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 1, 8: 0, 9: -1, 10: -2, 11: -2, 12: -2, 13: -2}
# or -centered and with 3 levels- w = {1: -1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 0, 8: 0, 9: 0, 10: -1, 11: -1, 12: -1, 13: -1}
# for each of them, the threshold is 6

# results for 4 decks, shuffle 52
# coefs: [-0.43015842, -0.14951642, 0.75302885, 1.45367159, 1.69597542, 0.71873267, 0.0932644, -0.18514274, -0.77762071, -1.90319907, 0.05352541, -1.38579426, -0.76848075]
# intercept: -6.93728315673
# thus we can choose -5 levels- w = {1: 0, 2: 0, 3: 1, 4: 1, 5: 2, 6: 1, 7: 0, 8: 0, 9: -1, 10: -2, 11: 0, 12: -1, 13: -1}
# or -3 levels- w = {1: 0, 2: 0, 3: 0, 4: 1, 5: 1, 6: 0, 7: 0, 8: 0, 9: 0, 10: -1, 11: 0, 12: -1, 13: 0}
# for this situation, we can choose a threshold of 6 or 7 (to be decided)
"""
