import time
from strategies.naive_strategy import plot_counter_parallel


# Counter parallel
n = 5 * 10e2
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
n = 10e6
start = time.time()
print("Running plot_counter_parallel with n = "+str(n))
print("this should take " + str(n * ratio / (60 * 60)) + " hours")
print("started at "+str(start))
plot_counter_parallel(n, show=False)
end = time.time()
print("done in: "+str(end-start))


