from strategy_generator.base_monte_carlo import MC
import json
epochs = 100000000
alpha = 10
policy = MC(epochs=epochs, epsilon=1.0/alpha)
policy["name"] = "my_basic"
policy["epochs"] = epochs
print(policy)
with open("strategy_tuning/"+str(epochs)+"_"+str(alpha)+".json", "w") as fp:
    json.dump(policy, fp)
