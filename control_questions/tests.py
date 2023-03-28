import control_questions as pages
from . import *
c = cu

class PlayerBot(Bot):
    def play_round(self):
        if self.participant.treatment == "human":
            answer_opponent = "human"
        else:
            answer_opponent = "robot"
    
        yield SubmissionMustFail(ControlQuestions, dict(
            same_pair=False,
            decision_type=self.participant.game,
            opponent_type=answer_opponent
        ))
        yield ControlQuestions, dict(
            same_pair=True,
            decision_type=self.participant.game,
            opponent_type=answer_opponent
        )