
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'dictator_instructions'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    NUM_ROUNDS_MAIN = 30
class Subsession(BaseSubsession):
    pass
def creating_session(subsession: Subsession):
    session = subsession.session
    for p in subsession.get_players():
        p.participant.game = "dictator"
        if session.config["treatments_human"] and not session.config["treatments_robot"]:
            p.participant.treatment = "human"
        elif not session.config["treatments_human"] and session.config["treatments_robot"]:
            if p.participant.id_in_session % 5 == 1:
                p.participant.treatment = "machine earns"
            elif p.participant.id_in_session % 5 == 2:
                p.participant.treatment = "burned"
            elif p.participant.id_in_session % 5 == 3:
                p.participant.treatment = "no info"
            elif p.participant.id_in_session % 5 == 4:
                p.participant.treatment = "token"
            elif p.participant.id_in_session % 5 == 0:
                p.participant.treatment = "programmer"
        else:
            if p.participant.id_in_session % 6 == 1:
                p.participant.treatment = "human"
            elif p.participant.id_in_session % 6 == 2:
                p.participant.treatment = "machine earns"
            elif p.participant.id_in_session % 6 == 3:
                p.participant.treatment = "burned"
            elif p.participant.id_in_session % 6 == 4:
                p.participant.treatment = "no info"
            elif p.participant.id_in_session % 6 == 5:
                p.participant.treatment = "token"
            elif p.participant.id_in_session % 6 == 0:
                p.participant.treatment = "programmer"
class Group(BaseGroup):
    pass
class Player(BasePlayer):
    pass
class Instructions(Page):
    form_model = 'player'
page_sequence = [Instructions]