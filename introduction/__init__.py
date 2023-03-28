
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'introduction'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    pass
class Player(BasePlayer):
    prolific_ID = models.StringField(label='Please enter your Prolific ID:')
class ID(Page):
    form_model = 'player'
    form_fields = ['prolific_ID']
class Introduction(Page):
    form_model = 'player'
    @staticmethod
    def vars_for_template(player: Player):
        session = player.session
        points_example = cu(100)
        return dict(
            participation_fee=session.config['participation_fee'],
            points_example=points_example,
            money_example=points_example.to_real_world_currency(session)
        )
page_sequence = [ID, Introduction]