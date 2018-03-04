import time
from strategies.naive_strategy import plot_counter_parallel


# Counter parallel
n = 5 * 10e5
start = time.time()
print("Running plot_counter_parallel with n = ")
print("this should take a few seconds")
print("started at "+str(start))
plot_counter_parallel(n, show=False)
end = time.time()
print("done in: "+str(end-start))
print("")

delta = end - start
ratio = delta / n

# Counter parallel
n = 5 * 10e8
start = time.time()
print("Running plot_counter_parallel with n = ")
print("this should take " + str(n * ratio) + " seconds")
print("started at "+str(start))
plot_counter_parallel(n, show=False)
end = time.time()
print("done in: "+str(end-start))

# Counter parallel 2
n = 5 * 10e9
start = time.time()
print("Running plot_counter_parallel with n = ")
print("this should take " + str(n * ratio) + " seconds")
print("started at "+str(start))
plot_counter_parallel(n, show=False, id='2')
end = time.time()
print("done in: "+str(end-start))

