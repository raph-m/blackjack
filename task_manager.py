import time
from strategies.naive_strategy import plot_counter_parallel
from strategies.counters import PersonalizedCounter, hi_opt_1, hi_opt_2, omega_2, ko, default_thorp, my_counter0, my_counter1

famous_counters = [default_thorp, hi_opt_1, hi_opt_2, ko, omega_2]
famous_counters.append(my_counter0)
famous_counters.append(my_counter1)
famous_counters_names = ["default_thorp", "hi_opt_1", "hi_opt_2", "ko", "omega_2"]
famous_counters_names.append("my_5_level_counter_with_b=6")
famous_counters_names.append("my_3_level_counter_with_b=6")
ratios = []

number_of_decks = 4
shuffle_every = 52

n = int(1e3)

for i in range(len(famous_counters)):

    # Counter parallel
    id_ = famous_counters_names[i] + "test"
    start = time.time()
    print("Running plot_counter_parallel with n = " + str(n) + " for counter " + famous_counters_names[i])
    print("this should take a few seconds")
    print("started at "+str(start))
    counter = PersonalizedCounter(counter_dic=famous_counters[i])
    plot_counter_parallel(n, show=False, id=id_, number_of_decks=number_of_decks, shuffle_every=shuffle_every, counter=counter)
    end = time.time()
    print("done in: "+str(end-start) + " seconds")
    print("")
    print("")

    ratios.append((end - start) / n)

print("")

n = int(1e5)
for i in range(len(famous_counters)):
    ratio = ratios[i]

    # Counter parallel
    id_ = famous_counters_names[i]
    start = time.time()
    print("Running plot_counter_parallel with n = " + str(n) + " for counter " + famous_counters_names[i])
    print("this should take " + str(n * ratio / (60 * 60)) + " hours")
    print("started at "+str(start))
    counter = PersonalizedCounter(counter_dic=famous_counters[i])
    plot_counter_parallel(n, show=False, id=id_, number_of_decks=number_of_decks, shuffle_every=shuffle_every, counter=counter)
    end = time.time()
    print("done in: "+str((end-start) / (60 * 60)) + " hours")
    print("")
    print("")


