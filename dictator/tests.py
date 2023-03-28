import dictator as pages
from . import *
c = cu

class PlayerBot(Bot):
    def play_round(self):
        import random

        yield Decision, dict(decision=random.choice(["X", "Y"]))
        if self.player.round_number == C.NUM_ROUNDS:
            # subsession_payoffround = subsession.in_round(self.player.payoff_round)
            # player_payoffround = player.in_round(self.player.payoff_round)
            # if player_payoffround.decision == "X":
            #     expect(self.player.payoff, self.subsession_payoffround.self_x)
            # else:
            #     expect(self.player.payoff, self.subsession_payoffround.self_y)      
            yield Results