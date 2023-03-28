import trust_human_firstmover as pages
from . import *
c = cu

class PlayerBot(Bot):
    def play_round(self):
        import random

        if self.participant.id_in_session % 4 in [1,3]:
            yield Trust, dict(
                trust=bool(random.getrandbits(1)), 
                belief_decision=random.choice(["X", "Y"])
            )