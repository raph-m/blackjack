import unittest
from environment.dealer import Dealer, Deck
from util.tools import get_value, get_values, get_score


class BasicTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        self.deck = Deck()

    # executed after each test
    def tearDown(self):
        pass

    def test_get_value(self):
        cards = [
            [1, 5, 5],
            [1, 3, 8],
            [2, 3, 8],
            [10, 1],
            [1, 10],
            [1, 10, 4],
            [4, 5, 12, 10],
            [13, 4],
            [1, 1, 1, 1, 1]
        ]
        truth = [
            11,
            12,
            13,
            11,
            11,
            15,
            29,
            14,
            5
        ]

        values = [get_value(c) for c in cards]
        print(values)

        for i in range(len(truth)):
            self.assertEqual(values[i], truth[i])

    def test_get_score(self):
        cards = [
            [1, 5, 5],
            [1, 3, 8],
            [2, 3, 8],
            [10, 1],
            [1, 10],
            [1, 10, 4],
            [4, 5, 12, 10],
            [13, 4],
            [1, 1, 1, 1, 1]
        ]
        truth = [
            21,
            12,
            13,
            22,
            22,
            15,
            0,
            14,
            15
        ]

        scores = [get_score(c) for c in cards]
        print(scores)

        for i in range(len(truth)):
            self.assertEqual(scores[i], truth[i])


if __name__ == "__main__":
    unittest.main()