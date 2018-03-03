# from strategy_generator.base_monte_carlo import MC
import json

# policy = MC(epochs=epochs, epsilon=1.0/alpha)
# policy["name"] = "my_basic"
# policy["epochs"] = epochs
# print(policy)
# with open("strategy_tuning/"+str(epochs)+"_"+str(alpha)+".json", "w") as fp:
#     json.dump(policy, fp)
epochs = 100000000
alpha = 10
with open("strategy_tuning/"+str(epochs)+"_"+str(alpha)+".json", "r") as fp:
    policy = json.load(fp)

from strategies.naive_strategy import parallel_expectancy
n_tries = 10000000
print(parallel_expectancy(policy, n_tries))
