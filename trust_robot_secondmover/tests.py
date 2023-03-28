import trust_robot_secondmover as pages
from . import *
c = cu

class PlayerBot(Bot):
    def play_round(self):
        import random

        yield Decision, dict(decision=random.choice(["X", "Y"]))
        if self.player.round_number == C.NUM_ROUNDS:
            yield Results