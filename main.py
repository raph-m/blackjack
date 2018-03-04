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
epochs = 100000
policy = QLearn(epochs=epochs, epsilon=0.1, alpha=0.1, gamma=0.99)
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


# implement dfo to find the best hyper parameters for MC and Q-learning
from strategy_tuning.dfo_tuning import tune
tune("qlearn")
#tune("MC")
