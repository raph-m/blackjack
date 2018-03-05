import time
from strategies.naive_strategy import plot_counter_parallel


# Counter parallel
n = 1e3
start = time.time()
print("Running plot_counter_parallel with n = "+str(n))
print("this should take a few seconds")
print("started at "+str(start))
plot_counter_parallel(n, show=False)
end = time.time()
print("done in: "+str(end-start))
print("")

delta = end - start
ratio = delta / n

# Counter parallel
n = 1e5
start = time.time()
print("Running plot_counter_parallel with n = "+str(n))
print("this should take " + str(n * ratio / (60 * 60)) + " hours")
print("started at "+str(start))
plot_counter_parallel(n, show=False)
end = time.time()
print("done in: "+str(end-start))


# implement dfo to find the best hyper parameters for MC and Q-learning
# from strategy_tuning.dfo_tuning import tune
# tune("qlearn")
# results: epsilon = 0.1989, alpha = 0.0362, gamma = 0.9587
# tune("MC")


