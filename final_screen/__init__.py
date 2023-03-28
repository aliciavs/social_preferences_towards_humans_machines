
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'final_screen'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    pass
class Player(BasePlayer):
    pass
class EndOfExperiment(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return participant.correct_answers
    @staticmethod
    def vars_for_template(player: Player):
        session = player.session
        return dict(
            bots=session.config["use_browser_bots"]
        )
class Drop(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return not participant.correct_answers
page_sequence = [EndOfExperiment, Drop]