class NoCounter:
    def __init__(self):
        self.rc = 0

    def increment(self, card):
        pass

    def get_rc(self):
        return self.rc

    def reset(self):
        self.rc = 0

default_thorp = {}

for i in range(1, 14):
    if i >= 10 or i == 1:
        default_thorp[i] = -1
    elif i <= 6:
        default_thorp[i] = +1
    else:
        default_thorp[i] = 0


class ThorpCounter:
    def __init__(self):
        self.rc = 0

    def increment(self, card):
        self.rc += default_thorp[card]

    def get_rc(self):
        return self.rc

    def reset(self):
        self.rc = 0
