import trust_human_secondmover as pages
from . import *
c = cu

class PlayerBot(Bot):
    def play_round(self):
        import random

        if self.participant.id_in_session % 4 not in [1,3]:
            yield Decision, dict(decision=random.choice(["X", "Y"]))