from strategies.naive_strategy import parallel_expectancy, expectancy
from strategy_generator.base_monte_carlo import MC
from strategy_generator.base_qlearning import QLearn
from environment.dealer import Dealer
import numpy as np
from skopt import gp_minimize
import json

epochs = 1000000
n_exp = 1000
n_calls = 30

def function_mc(x):
    dealer = Dealer(seed=10)
    epsilon = x[0]
    policy = MC(dealer, epochs, epsilon)
    policy["name"] = "my_basic"
    return - parallel_expectancy(policy, n_exp)


def function_qlearn(x):
    dealer = Dealer(seed=10)
    epsilon, alpha, gamma = x
    policy = QLearn(dealer, epochs, epsilon, alpha, gamma)
    policy["name"] = "my_basic"
    return - parallel_expectancy(policy, n_exp)


def tune(algo):
    alg = "DFO"
    if algo == "MC":
        res = gp_minimize(function_mc, [(0, 1)], n_calls=n_calls, x0=[0.5], verbose=True)
        epsilon = res.x[0]
        with open("temp_results/"+algo+"_hyper_parameters"+".json", "w") as fp:
            json.dump({"algorithm": algo,
                "epsilon" : epsilon,
                "value function" : -res.fun
                },
                fp)
        #print ('best epsilon is:', res.x)
        #print ('best expectancy is:', - res.fun)
    if algo == "qlearn" :
        res = gp_minimize(function_qlearn, [(0, .2),(0,.2),(.8,1)], n_calls=n_calls, verbose=True)
        epsilon, alpha, gamma = res.x
        with open("temp_results/"+algo+"_hyper_parameters"+".json", "w") as fp:
            json.dump({"algorithm" : algo,
                "epsilon" : epsilon,
                "alpha" : alpha,
                "gamma" : gamma,
                "value function" : -res.fun
                },
                fp)
        #print ('best epsilon is:', epsilon)
        #print ('best alpha is:', alpha)
        #print ('best gamma is:', gamma)
        #print ('best expectancy is:', - res.fun)
