from environment.dealer import Dealer
import numpy as np
"""
We assume here that there is ONLY ONE player playing against the dealer
We encode a pair state action by the following tuple:
((player hand), (dealer hand), action). Example: ((2,7,10),(4,8,3),"hit")
The cards are represented by there nature (from ace to king (1 to 13)) and the
actions hit, stick, double and split.
That way, the Q value of a state action pair is the average reward obtained
after this pair appeared.
At the beginning of each episode, we choose radomly an action, in this case, 0
is "hit", 1 is "stick", 2 is "double", 3 is "split"
"""
dealer = Dealer(seed=0)
actions = ["hit", "stick", "double", "split"]


def choose_action(state, Q, epsilon):
    # implement epsilon-greedy explore policy
    n_a = 4
    q = np.zeros(n_a)
    for i in range(n_a):
        p = (state[0], state[1], actions[i])
        if p in Q:
            q[i] = Q[p]

    prob = np.random.random()
    if prob > epsilon:
        return actions[np.argmax(q)]
    else:
        return actions[np.random.randint(4)]


def episode(Q, F, epsilon):
    res = dealer.reset()
    observation = []
    if res["done"]:
        dh = tuple(np.sort(res["dealer_hand"]))
        ph = tuple(np.sort(res["hands"][0][0]))
        reward = res["rewards"][0]
        pair = (ph, dh, "stick")
        observation.append(pair)
    else:
        action = actions[np.random.randint(4)]
        reward = 0
        player_playing = res["player_playing"]
        hand_playing = res["hand_playing"]
        dealer_cards = res["dealer_cards"]
        hand = res["hands"][player_playing][hand_playing]
        observation.append((tuple(np.sort(hand)),
            tuple(np.sort(dealer_cards)),
            action))
        for t in range(12):
            res = dealer.step(action)
            if res["done"]:
                break
            player_playing = res["player_playing"]
            hand_playing = res["hand_playing"]
            dealer_cards = res["dealer_cards"]
            hand = res["hands"][player_playing][hand_playing]
            state = (tuple(hand), tuple(dealer_cards))
            action = choose_action(state, Q, epsilon)
            observation.append((tuple(np.sort(hand)),
                tuple(np.sort(dealer_cards)),
                action))

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
        state = (p[0], p[1])
        action = p[2]
        reward = Q[p]
        if state in policy:
            a = policy[state]
            pair = (p[0], p[1], a)
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
        if i % 1000 == 0:
            print("episode", i)
    policy = get_policy(Q)
    return policy
