from environment.dealer import Dealer
from util.tools import encoding
import numpy as np
"""
We assume here that there is ONLY ONE player playing against the dealer
We encode a pair state action by the following tuple:
(state, action) where state is encoded by the string : "type.player_score.dealer_hand"
The cards are represented by there nature (from ace to king (1 to 13)) and the
actions hit, stickdealer_cardsd split.
That way, the Q value of a state action pair is the average reward obtained
after this pair appeared.
At the beginning of each episode, we choose radomly an action, in this case, 0
is "hit", 1 is "stick", 2 is "double", 3 is "split"
"""
dealer = Dealer(seed=0)
actions = ["hit", "stick", "double", "split"]


def choose_action(state, Q, epsilon, random=False):
    # implement epsilon-greedy explore policy
    # First case, the player has a double
    dec = state.split(".")
    typ, player, dealer = dec[0], int(dec[1]), int(dec[2])
    if typ=="pair":
        n_a = 4
    else:
        n_a = 3
    if random:
        return actions[np.random.randint(n_a)]
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

def episode(Q, F, epsilon):
    res = dealer.reset()
    observation = []
    if res["done"]:
        dealer_cards = res["dealer_cards"]
        player_cards = res["hands"][0][0]
        reward = int(sum(res["rewards"][0]))
        pair = (encoding(player_cards, [dealer_cards[0]]), "stick")
        observation.append(pair)
    else:
        player_playing = res["player_playing"]
        hand_playing = res["hand_playing"]
        dealer_cards = res["dealer_cards"]
        player_cards = res["hands"][player_playing][hand_playing]
        state = encoding(player_cards, [dealer_cards[0]])
        action = choose_action(state, Q, epsilon, random=True)
        observation.append((state, action))
        for t in range(21):
            #print("step", action, hand)
            res = dealer.step(action)
            if res["done"]:
                reward = int(sum(res["rewards"][0]))
                break
            player_playing = res["player_playing"]
            hand_playing = res["hand_playing"]
            dealer_cards = res["dealer_cards"]
            player_cards = res["hands"][player_playing][hand_playing]
            can_split = len(res["hands"][player_playing])==1
            state = encoding(player_cards, [dealer_cards[0]], can_split)
            action = choose_action(state, Q, epsilon)
            observation.append((state, action))

    visited = []
    for sa in observation:
        if sa not in visited:
            visited.append(sa)
            if sa not in F:
                F[sa] = 1
            else:
                F[sa] += 1
            if sa not in Q:
                Q[sa] = reward
            else:
                Q[sa] += 1/F[sa]*(reward - Q[sa])
    return Q, F


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


def MC(dealer=dealer, epochs=100, epsilon=0.1):
    Q = {}
    F = {}
    for i in range(epochs):
        Q, F = episode(Q, F, epsilon)
        #if i % 10000 == 0:
            #print("episode", i)
    policy = get_policy(Q)
    #print(Q)
    return policy
