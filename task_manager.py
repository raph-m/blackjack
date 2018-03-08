import time

from strategies.strategies import best_naive_strategy, read_counter_results, plot_counter_parallel
from strategies.compare_counters import compare_counters
from strategies.counters import PersonalizedCounter, hi_opt_1, hi_opt_2, omega_2, ko, default_thorp,\
    my_counter0, my_counter1


n = int(1e3)  #  1e5 TODO: you can reduce the values of n by a factor 10 if you want to obtain the results faster
# TODO: but they will be less precise...
print("computing best naive strategy:")
best_naive_strategy(n)

# WIKI BASIC
# TUNE strategy


n = int(1e3)  # 1e5
number_of_decks = [2, 2, 3, 4, 4, 6]
shuffle_every = [52, 80, 104, 52, 104, 80]
ids = ["thorp"+str(number_of_decks[i])+"decks"+str(shuffle_every[i])+"shuffleevery" for i in range(len(number_of_decks))]

for i in range(len(number_of_decks)):
    start = time.time()
    print("Running plot counter with n = "+str(n) + ", for " + ids[i])
    plot_counter_parallel(
        n,
        show=False,
        id=ids[i],
        number_of_decks=number_of_decks[i],
        shuffle_every=shuffle_every[i]
    )
    end = time.time()
    print("done in: "+str((end-start) / (60 * 60)) + " hours\n")


# plot results
for i in range(len(number_of_decks)):
    read_counter_results(id=ids[i], get_baseline=True)


famous_counters = [default_thorp, hi_opt_1, hi_opt_2, ko, omega_2]
famous_counters.append(my_counter0)
famous_counters.append(my_counter1)
famous_counters_names = ["default_thorp", "hi_opt_1", "hi_opt_2", "ko", "omega_2"]
famous_counters_names.append("my_5_level_counter_with_b=6")
famous_counters_names.append("my_3_level_counter_with_b=6")

number_of_decks = 4
shuffle_every = 52

n = int(1e4)  # 1e5
for i in range(len(famous_counters)):

    # Counter parallel
    id_ = famous_counters_names[i]
    start = time.time()
    print("Running plot_counter with n = " + str(n) + " for counter " + famous_counters_names[i])
    counter = PersonalizedCounter(counter_dic=famous_counters[i])
    plot_counter_parallel(
        n,
        show=False,
        id=id_,
        number_of_decks=number_of_decks,
        shuffle_every=shuffle_every,
        counter=counter
    )
    end = time.time()
    print("done in: "+str((end-start) / (60 * 60)) + " hours")
    print("")
    print("")


for i in range(len(famous_counters)):
    read_counter_results(id=famous_counters_names[i], baseline=-0.0087)


n = int(1e2)
print("running compare counters for n =" + str(n))
print("this should take a few seconds")
start = time.time()
compare_counters(n, 4, 52)
end = time.time()
print("done in: "+str((end-start) / (60 * 60)) + " hours")

ratio = (end - start) / n
n = int(1e4)  # 1e7
print("running compare counters for n =" + str(n))
start = time.time()
print("this should take " + str(n * ratio / (60 * 60)) + " hours")
compare_counters(n, 4, 52)
end = time.time()
print("done in: "+str((end-start) / (60 * 60)) + " hours")



















