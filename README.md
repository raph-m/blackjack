# blackjack
Count cards in blackjack to bring down the house
ALL the code on this project was created by us.

## Retrieve our results
Our project report is available in the results folder. You will be able to compute all of the results presented in the report simply by running the 'task_manager.py' file. However, this can take a very long time, so you might want to skip some parts of this file.

## Environment
In the environment folder you can find the classes 'Dealer' and 'Deck'. You can find an example on how tu use them in the 'play_blackjack.py' file.

## Tools
In the 'util/tools.py' file, you will find some useful tools for blackjack. For example, you can get the score of a hand or it's type (soft, hard, pair).

## Strategies
In the 'strategies/strategies.py' file you can find some implementations of strategies like the naive strategy (dealer-like strategy). You can also find some functions to evaluate strategies.

## Counters
In the 'strategies.counters.py' file, you can find the implementation of several counters. Some of them are 'famous' counters and the others were generated by our machine learning algorithms.

## Cloud setup
In the 'cloud_setup.py' file you can find the command line instructions to be able to run our entire project for Ubuntu 16.04 LTS. This can be useful if you want to setup a distant server to multiprocess the computations.

## Strategy Generator
In the 'strategy_generator/base_qlearning.py' you can find the implementation of the Q-learning algorithm. To run it, call the QLearn() function.
In the 'strategy_generator/base_monte_carlo.py' you can find the implementation of the Monte Carlo reinforcement algorithm. To run it, call the MC() function.

## Strategy Tuning
In the 'strategy_tunning/dfo_tuning.py' file you can find the implementation of hyperparameters tuning usig DFO-TR algorithm. To run it, call tune("MC") or tune("qlearn").

## Results
You will find plots of the different basic strategies and of counters performance in the folder results.
