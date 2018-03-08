import time
from strategies.strategies import plot_counter_parallel


# Counter parallel
n = 1e3
id_ = "test"
number_of_decks = 3
shuffle_every = 104
start = time.time()
print("Running plot_counter_parallel with n = "+str(n))
print("this should take a few seconds")
print("started at "+str(start))
plot_counter_parallel(n, show=False, id=id_, number_of_decks=number_of_decks, shuffle_every=shuffle_every)
end = time.time()
print("done in: "+str(end-start) + " seconds")
print("")

delta = end - start
ratio = delta / n

# Counter parallel
n = int(1e5)
id_ = "3decks"
number_of_decks = 3
shuffle_every = 104
start = time.time()
print("Running plot_counter_parallel with n = "+str(n))
print("this should take " + str(n * ratio / (60 * 60)) + " hours")
print("started at "+str(start))
plot_counter_parallel(n, show=False, id=id_, number_of_decks=number_of_decks, shuffle_every=shuffle_every)
end = time.time()
print("done in: "+str((end-start) / (60 * 60)) + " hours")


# Counter parallel
n = int(1e5)
id_ = "2decks"
number_of_decks = 2
shuffle_every = 80
start = time.time()
print("Running plot_counter_parallel with n = "+str(n))
print("this should take " + str(n * ratio / (60 * 60)) + " hours")
print("started at "+str(start))
plot_counter_parallel(n, show=False, id=id_, number_of_decks=number_of_decks, shuffle_every=shuffle_every)
end = time.time()
print("done in: "+str((end-start) / (60 * 60)) + " hours")


