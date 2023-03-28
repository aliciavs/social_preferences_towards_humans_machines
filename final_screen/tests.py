import final_screen as pages
from . import *
c = cu

class PlayerBot(Bot):
    def play_round(self):
        if self.participant.correct_answers:
            yield EndOfExperiment
        if not self.participant.correct_answers:
            yield Drop