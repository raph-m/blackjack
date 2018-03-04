from strategy_generator.base_monte_carlo import MC
import json
epochs = 1000000
alpha = 3
policy = MC(epochs=epochs, epsilon=1.0/alpha)
policy["name"] = "my_basic"
policy["epochs"] = epochs
policy["alpha"] = alpha
print(policy)
with open("strategy_tuning/"+str(epochs)+"_"+str(alpha)+".json", "w") as fp:
    json.dump(policy, fp)

with open("strategy_tuning/"+str(epochs)+"_"+str(alpha)+".json", "r") as fp:
    policy = json.load(fp)

print(policy["soft.19.4"])
policy["name"] = "my_basic"

from strategies.naive_strategy import parallel_expectancy, expectancy
import time
start = time.time()
n_tries = 1000000
strategy = {"name": "basic"}
print(parallel_expectancy(policy, n_tries))
end = time.time()
print("parallel time: ")
print(end-start)
