import numpy as np

from util.tools import get_score
from strategies.counters import NoCounter
from util.tools import is_soft_17
color = np.arange(1, 14, 1, dtype="int")


class Deck:
    def __init__(self, number_of_decks=6, shuffle_every=78, seed=10, counter=NoCounter()):
        self.number_of_decks = number_of_decks
        self.shuffle_every = shuffle_every
        self.index = 5
        self.cards = color
        self.counter = counter
        np.random.seed(seed)

        for i in range(self.number_of_decks * 4 - 1):
            self.cards = np.append(self.cards, color)

        self.shuffle()

    def shuffle(self):
        self.counter.reset()
        np.random.shuffle(self.cards)
        self.index = 0

    def next_card(self):
        self.index += 1
        self.counter.increment(self.cards[self.index])
        return self.cards[self.index]

    def force_game(self, cards):
        for j in range(len(cards)):
            for i in range(len(self.cards)):
                if cards[j] == self.cards[i]:
                    self.cards[i] = self.cards[j]
                    self.cards[j] = cards[j]


class Dealer:
    def __init__(
            self,
            number_of_players=1,
            number_of_decks=6,
            shuffle_every=78,
            seed=10,
            counter=NoCounter(),
            blackjack_reward=1.5
    ):
        self.blackjack_reward = blackjack_reward
        self.deck = Deck(number_of_decks, shuffle_every, seed=seed, counter=counter)
        self.shuffle_every = shuffle_every
        self.number_of_decks = number_of_decks
        self.number_of_players = number_of_players
        self.number_of_hands = number_of_players
        self.hands = {}
        self.dealer_cards = []
        self.doubled_hands = {}
        self.hand_rewards = {}
        self.dealer_score = None

        for i in range(number_of_players):
            self.doubled_hands[i] = []
            self.hand_rewards[i] = []

        self.player_playing = 0
        self.hand_playing = 0

    def shuffle_if_needed(self):
        if self.deck.index > self.shuffle_every:
            self.deck.shuffle()

    def reset(self):
        self.shuffle_if_needed()
        self.hands = {}
        self.dealer_cards = []
        self.doubled_hands = {}
        self.hand_rewards = {}
        self.dealer_score = None

        for i in range(self.number_of_players):
            self.doubled_hands[i] = []
            self.hand_rewards[i] = []

        self.player_playing = 0
        self.hand_playing = 0

        for i in range(self.number_of_players):
            self.hands[i] = [[self.deck.next_card()]]

        self.dealer_cards.append(self.deck.next_card())

        for i in range(self.number_of_players):
            # TODO: check that this is the way to do this
            self.hands[i][0].append(self.deck.next_card())

        # pour le blackjack américain il faut rajouter ça ici:
        # self.dealer_cards.append(self.deck.next_card())

        for i in range(self.number_of_players):
            self.player_playing = i
            if get_score(self.hands[i][0]) not in [0, 22]:
                done = False
                break
            else:
                done = True

        if self.player_playing == self.number_of_players - 1 and done:
            return self.results()

        return {
            "done": False,
            "dealer_cards": self.dealer_cards,
            "hands": self.hands,
            "hand_playing": self.hand_playing,
            "player_playing": self.player_playing
        }

    def reset_completely(self):
        self.deck.shuffle()
        return self.reset()

    def hit(self, player_id, hand_id):
        self.hands[player_id][hand_id].append(self.deck.next_card())
        score = get_score(self.hands[player_id][hand_id])
        # TODO: remplacer par score in [0, 21, 22] ?
        return score in [0, 22]

    def split(self, player_id, hand_id):

        try:
            assert len(self.hands[player_id]) == 1
        except AssertionError:
            raise ValueError("you can't split more than once")

        try:
            assert len(self.hands[player_id][hand_id]) == 2
        except AssertionError:
            raise ValueError("you should have exactly two cards to be able to split")

        try:
            if self.hands[player_id][hand_id][0] < 10 or self.hands[player_id][hand_id][1] < 10:
                assert self.hands[player_id][hand_id][0] == self.hands[player_id][hand_id][1]
        except AssertionError:
            raise ValueError("you should have a double in order to split")

        ass_pair = self.hands[player_id][hand_id][0] == 1

        value = self.hands[player_id][hand_id][0]

        self.hands[player_id][hand_id] = [value]
        self.hands[player_id].append([value])

        served = self.hit(player_id, hand_id)
        self.hit(player_id, len(self.hands[player_id]) - 1)
        return served, ass_pair

    def evaluate(self, player_id, hand_id):
        doubled = hand_id in self.doubled_hands[player_id]
        x = 2 if doubled else 1
        player_score = get_score(self.hands[player_id][hand_id])

        if player_score == 22 and len(self.hands[player_id]) >= 2:
            player_score = 21

        if player_score == 0:
            return -x
        if player_score == 22 and self.dealer_score < 22:
            return 1.5 * x
        if self.dealer_score > player_score:
            return -x
        if self.dealer_score == player_score:
            return 0
        return x

    def results(self):
        while 0 < get_score(self.dealer_cards) < 17 or is_soft_17(self.dealer_cards):
            self.dealer_cards.append(self.deck.next_card())

        self.dealer_score = get_score(self.dealer_cards)

        for i in range(self.number_of_players):
            current = []
            for j in range(len(self.hands[i])):
                current.append(self.evaluate(i, j))
            self.hand_rewards[i] = current

        shuffle = False
        if self.deck.index > self.shuffle_every:
            shuffle = True

        return {
            "shuffle": shuffle,
            "done": True,
            "dealer_cards": self.dealer_cards,
            "dealer_score": self.dealer_score,
            "hands": self.hands,
            "rewards": self.hand_rewards,
            "count": self.deck.counter.get_rc()
        }

    def step(self, action):
        try:
            assert action in ["hit", "double", "split", "stick"]
        except AssertionError:
            raise ValueError("action should be 'hit', 'double', 'split' or 'stick'")

        served = False
        if action in ["hit", "double"]:
            served = self.hit(self.player_playing, self.hand_playing)
            if action == "double":
                self.doubled_hands[self.player_playing].append(self.hand_playing)
                served = True

        if action == "stick":
            served = True

        if action == "split":
            served, ass_pair = self.split(self.player_playing, self.hand_playing)

            if ass_pair:
                self.player_playing += 1
                self.hand_playing = 0
                if self.player_playing >= self.number_of_players:
                    return self.results()

        if served:
            if len(self.hands[self.player_playing]) - 1 == self.hand_playing:
                self.player_playing += 1
                self.hand_playing = 0

                if self.player_playing >= self.number_of_players:
                    return self.results()
            else:
                self.hand_playing += 1

        return {
            "done": False,
            "dealer_cards": self.dealer_cards,
            "hands": self.hands,
            "hand_playing": self.hand_playing,
            "player_playing": self.player_playing
        }


