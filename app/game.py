import random

class Throw:
    def __eq__(self, other):
        if self.__class__ == other.__class__:
            return True
        return False

class Rock(Throw):
    alias = "rock"
    def __gt__(self, other):
        if isinstance(other, Scissors):
            return True
        return False

class Paper(Throw):
    alias = "paper"
    def __gt__(self, other):
        if isinstance(other, Rock):
            return True
        return False

class Scissors(Throw):
    alias = "scissors"
    def __gt__(self, other):
        if isinstance(other, Paper):
            return True
        return False


class Player:
    def __init__(self, username: str):
        self.username = username
        self._throw = None
        self.last_throw = None
        self._last_opponent = None
        self._last_result = None

    @property
    def throw(self):
        if self.username is None:
            # It's the computer which will share this class
            if self._throw is None:
                throw = random.choice([Rock, Paper, Scissors])
                self._throw = throw()
        return self._throw

    @throw.setter
    def throw(self, selection: str):
        if selection == "rock":
            self._throw = Rock()
        if selection == "paper":
            self._throw = Paper()
        if selection == "scissors":
            self._throw = Scissors()

    @property
    def last_result(self):
        return result_lut[self._last_result]

    @last_result.setter
    def last_result(self, result):
        if result is self:
            self._last_result = 1
        if result is None:
            self._last_result = 0
        self._last_result = -1

    def on_game_end(self, result, opponent=None):
        if self.username is not None: # Computer
            self._last_opponent = opponent
        self.last_throw = self.throw
        self.last_result = result
        self._throw = None # reset the throw


def get_outcome(p1: Player, p2: Player):
    """
    Takes two players, compares throws, returns winnig player or None if tie
    """
    if p1.throw < p2.throw:
        return p2
    if p1.throw > p2.throw:
        return p1


