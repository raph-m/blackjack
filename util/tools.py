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
