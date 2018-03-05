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
epochs = 1000000
policy = QLearn(epochs=epochs, epsilon=0.1989, alpha=0.0362, gamma=0.9587)
policy["name"] = "my_basic"
policy["epochs"] = epochs
"""

"""
# Load a strategy designed with n epochs
epochs = 100000000
alpha = 10
with open("strategy_tuning/"+str(epochs)+"_"+str(alpha)+".json", "r") as fp:
    policy = json.load(fp)

print(policy["soft.19.4"])
policy["name"] = "my_basic"
"""

#save wiki base strategy the load it
from strategies.naive_strategy import save_base_policy
#save_base_policy()
with open("strategy_tuning/base_wiki_policy.json", "r") as fp:
    policy = json.load(fp)
policy["name"] = "wiki_base"
policy["epochs"] = 0

"""
# Evaluate the policy with parallel computing
from strategies.naive_strategy import parallel_expectancy, expectancy
import time
start = time.time()
n_tries = 10000 # 00
print(parallel_expectancy(policy, n_tries))
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
