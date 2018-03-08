default_thorp = {}
hi_opt_1 = {}
hi_opt_2 = {}
ko = {}
omega_2 = {}


# those are the counters that we found after training:
# counter 5 level counter for 4 decks and 52 shuffle every
my_counter0 = {1: 0, 2: 0, 3: 1, 4: 1, 5: 2, 6: 1, 7: 0, 8: 0, 9: -1, 10: -2, 11: 0, 12: -1, 13: -1}

# counter 3 level counter for 4 decks and 52 shuffle every
my_counter1 = {1: 0, 2: 0, 3: 0, 4: 1, 5: 1, 6: 0, 7: 0, 8: 0, 9: 0, 10: -1, 11: 0, 12: -1, 13: 0}


for i in range(1, 14):
    if i >= 10 or i == 1:
        default_thorp[i] = -1
    elif 1 < i <= 6:
        default_thorp[i] = +1
    else:
        default_thorp[i] = 0

for i in range(1, 14):
    if i >= 10:
        hi_opt_1[i] = -1
    elif 3 <= i <= 6:
        hi_opt_1[i] = +1
    else:
        hi_opt_1[i] = 0

for i in range(1, 14):
    if i >= 10:
        hi_opt_2[i] = -2
    elif i in [4, 5]:
        hi_opt_2[i] = 2
    elif i in [2, 3, 6, 7]:
        hi_opt_2[i] = 1
    else:
        hi_opt_2[i] = 0

for i in range(1, 14):
    if i >= 10 or i == 1:
        ko[i] = -1
    elif 1 < i <= 7:
        ko[i] = +1
    else:
        ko[i] = 0

for i in range(1, 14):
    if i >= 10:
        omega_2[i] = -2
    elif i == 9:
        omega_2[i] = -1
    elif i in [2, 3, 7]:
        omega_2[i] = +1
    elif i in [4, 5, 6]:
        omega_2[i] = +2
    else:
        omega_2[i] = 0


class NoCounter:
    def __init__(self):
        self.rc = 0

    def increment(self, card):
        pass

    def get_rc(self):
        return self.rc

    def reset(self):
        self.rc = 0


class ThorpCounter:
    def __init__(self):
        self.rc = 0

    def increment(self, card):
        self.rc += default_thorp[card]

    def get_rc(self):
        return self.rc

    def reset(self):
        self.rc = 0


class PersonalizedCounter:
    def __init__(self, counter_dic):
        self.rc = 0
        self.counter_dic = counter_dic

    def increment(self, card):
        self.rc += self.counter_dic[card]

    def get_rc(self):
        return self.rc

    def reset(self):
        self.rc = 0


class CountAllCards:
    def __init__(self):
        self.rc = {}
        for j in range(1, 14):
            self.rc[j] = 0

    def increment(self, card):
        self.rc[card] += 1

    def get_rc(self):
        return self.rc

    def reset(self):
        for j in range(1, 14):
            self.rc[j] = 0
