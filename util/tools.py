def get_value(cards):
    """
    :param cards: (list of ints) the cards to evaluate
    :return: value (int) the value of the cards where we count aces as one point.
    """
    value = 0

    for i in range(len(cards)):
        if cards[i] < 11:
            value += cards[i]
        else:
            value += 10

    return value


def get_values(cards):
    """
    :param cards: (list of ints) the cards to evaluate
    :return: values (list of ints) the possible values of the set of cards where an ace can count as one point
    or eleven points
    """
    values = [get_value(cards)]
    for i in range(len(cards)):
        if cards[i] < 2:
            current = []
            for p in values:
                current.append(p+10)
            for c in current:
                values.append(c)
    return values


def get_score(cards):
    """
    :param cards: (list of ints) the cards to evaluate
    :return: score (int) the best possible score of the set of cards. 22 is blackjack and 0 means that the
    player burst.
    """

    max_score = 0
    min_score = 30

    for v in get_values(cards):
        if 22 > v > max_score:
            max_score = v
        if v < min_score:
            min_score = v

    if min_score > 21:
        return 0

    if max_score == 21 and len(cards) < 3:
        return 22

    return max_score


def encoding(player, dealer, can_split=True):
    dealer_encoding = str(get_value(dealer))

    if len(player) == 2 and can_split:
        if player[0] == player[1] or (player[0] >= 10 and player[1] >= 10):
            value = min(10, player[0])
            return "pair."+str(value)+"."+dealer_encoding

    player_score = get_score(player)
    if get_value(player) == player_score:
        return "hard."+str(player_score)+"."+dealer_encoding

    return "soft."+str(player_score)+"."+dealer_encoding


def is_soft_17(cards):
    if get_score(cards) == 17:
        if get_value(cards) < get_score(cards):
            return True
    return False


def check_encoding():
    assert encoding([1, 1, 1], [8]) == "soft.13.8"
    assert encoding([10, 1, 1], [12]) == "hard.12.10"
    assert encoding([13, 12, 1], [1]) == "hard.21.1"
    assert encoding([13, 8, 1], [1]) == "hard.19.1"
    assert encoding([13, 11], [1]) == "pair.10.1"
    assert encoding([7, 7], [1]) == "pair.7.1"

check_encoding()
