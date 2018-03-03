from strategies.naive_strategy import expectancy
from strategy_generator.base_monte_carlo import MC
from environment.dealer import Dealer
import numpy as np
from skopt import gp_minimize

epochs = 100000
n_exp = 10

def function(x):
    dealer = Dealer(seed=0)
    x = x[0]
    policy = MC(dealer, epochs, x)
    policy["name"]="my_basic"
    return - expectancy(policy, n_exp)

def tune():
    alg = "DFO"
    res = gp_minimize(function, [(0,0.6)], n_calls=30)
    print ('best epsilon is:', res.x)
    print ('best expectancy is:', res.fun)
