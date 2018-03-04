from environment.dealer import Dealer
from util.tools import encoding
import numpy as np

"""
We assume here that there is ONLY ONE player playing against the dealer
We encode a pair state action by the following tuple:
(state, action). Example: (pair.7.10,"hit") where state is encoded by
type.player_score.dealer_hand
The cards are represented by there nature (from ace to king (1 to 13)) and the
actions hit, stick, double and split.
The Q value is here obtained by Q-learning algorithm
At the beginning of each episode, we choose radomly a state.
"""
dealer = Dealer(seed=0)
actions = ["hit", "stick", "double", "split"]

def update_Q(Q, state, state_tmp, action, reward, alpha, gamma):
    maxi = 0
    for act in actions:
        p = (state_tmp, act)
        if p in Q and Q[p] > maxi:
            maxi = Q[p]
    pair = (state, action)
    if pair in Q:
        Q[pair] = Q[pair] + alpha*(reward + gamma*maxi - Q[pair])
    else:
        Q[pair] = alpha*(reward + gamma*maxi)
    return Q

def choose_action(state, Q, epsilon):
    # implement epsilon-greedy explore policy
    # First case, the player has a double
    dec = state.split(".")
    typ, player, dealer = dec[0], int(dec[1]), int(dec[2])
    if typ=="pair":
        n_a = 4
    else:
        n_a = 3
    q = np.zeros(n_a)
    for i in range(n_a):
        p = (state, actions[i])
        if p in Q:
            q[i] = Q[p]

    prob = np.random.random()
    if prob > epsilon:
        action = actions[np.argmax(q)]
        #print("det", state, action)
        return action
    else:
        action = actions[np.random.randint(n_a)]
        #print("rand", state, action)
        return action

def episode(Q, epsilon, alpha, gamma):
    res = dealer.reset()
    if res["done"]:
        dealer_cards = res["dealer_hand"]
        player_cards = res["hands"][0][0]
        reward = int(sum(res["rewards"][0]))
        state = encoding(player_cards, [dealer_cards[0]])
        pair = (state,"stick")
        Q[pair] = reward
    else:
        player_playing = res["player_playing"]
        hand_playing = res["hand_playing"]
        dealer_cards = res["dealer_cards"]
        player_cards = res["hands"][player_playing][hand_playing]
        state = encoding(player_cards, [dealer_cards[0]])
        for t in range(12):
            action = choose_action(state, Q, epsilon)
            res = dealer.step(action)
            if res["done"]:
                pair = (state, action)
                reward = int(sum(res["rewards"][0]))
                if pair in Q:
                    Q[pair] = Q[pair]*(1-alpha) + alpha*reward
                else:
                    Q[pair] = alpha*reward
                break
            player_playing = res["player_playing"]
            hand_playing = res["hand_playing"]
            dealer_cards = res["dealer_cards"]
            player_cards = res["hands"][player_playing][hand_playing]
            can_split = len(res["hands"][player_playing])==1
            state_tmp = encoding(player_cards, [dealer_cards[0]], can_split)
            reward = 0
            Q = update_Q(Q, state, state_tmp, action, reward, alpha, gamma)
            state = state_tmp
    return Q

def get_policy(Q):
    policy = {}
    for p in Q:
        state = p[0]
        action = p[1]
        reward = Q[p]
        if state in policy:
            act = policy[state]
            pair = (state, act)
            if Q[pair] < Q[p]:
                policy[state] = action
        else :
            policy[state] = action
    return policy


def QLearn(dealer=dealer, epochs=100, epsilon=0.1, alpha=0.1, gamma=0.99):
    Q = {}
    for i in range(epochs):
        Q = episode(Q, epsilon, alpha, gamma)
        #if i % 10000 == 0:
            #print("episode", i)
    policy = get_policy(Q)
    #print(Q)
    return policy
