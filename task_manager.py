import time

from strategies.strategies import best_naive_strategy, read_counter_results, plot_counter_parallel
from strategies.compare_counters import compare_counters
from strategies.counters import PersonalizedCounter, hi_opt_1, hi_opt_2, omega_2, ko, default_thorp,\
    my_counter0, my_counter1


n = int(1e5)
print("computing best naive strategy:")
best_naive_strategy(n)

from util.tools import visualizePolicy
from strategies.naive_strategy import save_base_policy
from strategies.naive_strategy import parallel_expectancy
save_base_policy() #to be run once
#load the generated policy
with open("strategy_generator/base_wiki_policy.json", "r") as fp:
    wiki_pol = json.load(fp)
visualizePolicy(wiki_pol)
wiki_pol["name"] = "my_basic"
wiki_pol["epochs"] = 1

n_tries = int(1e6)
print("expectancy for reference basic strategy:", parallel_expectancy(wiki_pol, n_tries))



# implement dfo to find the best hyper parameters for MC and Q-learning
# WARNING : Can take almost 16 hours to run, better load the already calculated parameters as shown bellow
from strategy_tuning.dfo_tuning import tune
tune("qlearn")
# results: epsilon = 0.197, alpha = 0.0019, gamma = 0.959
tune("MC")
# results: epsilon = 0.01

epochs = int(1e7) # a lower value does not alway permit to cover all the states
# generate a policy with a Monte Carlo RL algorithm and Visualize it
from strategy_generator.base_monte_carlo import MC
with open("strategy_tuning/mc_hyper_parameters.json", "r") as fp:
    hyp_mc = json.load(fp)
mc_pol = MC(epochs=epochs, epsilon=hyp_mc["epsilon"])
visualizePolicy(mc_pol)
mc_pol["name"] = "my_basic"
mc_pol["epochs"] = 1
print("expectancy for Monte Carlo basic strategy:", parallel_expectancy(mc_pol, n_tries))

from strategy_generator.base_qlearning import QLearn
with open("strategy_tuning/qlearn_hyper_parameters.json", "r") as fp:
    hyp_cl = json.load(fp)
ql_pol = QLearn(epochs=epochs, epsilon=hyp_ql["epsilon"], alpha=hyp_ql["alpha"], gamma=hyp_ql["gamma"])
visualizePolicy(ql_pol)
ql_pol["name"] = "my_basic"
ql_pol["epochs"] = 1
print("expectancy for Q-learning basic strategy:", parallel_expectancy(ql_pol, n_tries))

number_of_decks = [2, 2, 3, 4, 4, 6]
shuffle_every = [52, 80, 104, 52, 104, 80]
ids = ["thorp"+str(number_of_decks[i])+"decks"+str(shuffle_every[i])+"shuffleevery" for i in range(len(number_of_decks))]

for i in range(len(number_of_decks)):
    start = time.time()
    print("Running plot counter with n = "+str(n)+ids[i])
    plot_counter_parallel(
        n,
        show=False,
        id=ids,
        number_of_decks=number_of_decks,
        shuffle_every=shuffle_every
    )
    end = time.time()
    print("done in: "+str((end-start) / (60 * 60)) + " hours")


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

n = int(1e5)
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
n = int(1e5)  # 1e7
print("running compare counters for n =" + str(n))
start = time.time()
print("this should take " + str(n * ratio / (60 * 60)) + " hours")
compare_counters(n, 4, 52)
end = time.time()
print("done in: "+str((end-start) / (60 * 60)) + " hours")
