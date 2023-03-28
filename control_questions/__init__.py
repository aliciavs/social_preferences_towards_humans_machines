
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'control_questions'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    NUM_TRIES = 2
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    pass
class Player(BasePlayer):
    same_pair = models.BooleanField(label='Will your pair of Player 1 and Player 2 remain the same throughout the whole experiment? ', widget=widgets.RadioSelect)
    decision_type = models.StringField(label='Which kind of decisions will be made and who will make them?', widget=widgets.RadioSelect)
    opponent_type = models.StringField(label='With what type of other player will you play?', widget=widgets.RadioSelect)
    tries_left = models.IntegerField(initial=C.NUM_TRIES)
def decision_type_choices(player: Player):
    import random 
    choices = [
        ["dictator", "Player 1 decides how to split a certain amount between him-/herself and Player 2."],
        ["joint", "Both players jointly decide how to split a certain amount between themselves."],
        ["ultimatum", "Player 1 makes an offer to Player 2 on how to split a certain amount between him-/herself and Player 2. Player 2 decides which offer s/he is willing to accept."],
        ["trust", "Player 2 either decides how to split a certain amount between him-/herself and Player 1, or delegates this decision to Player 1."]
    ]
    random.shuffle(choices)
    return choices
def opponent_type_choices(player: Player):
    participant = player.participant
    import random 
    choices = [
        ["human", "Another participant of this study."],
        ["robot", "A computer."]
    ]
    random.shuffle(choices)
    return choices
class ControlQuestions(Page):
    form_model = 'player'
    @staticmethod
    def get_form_fields(player: Player):
        if player.tries_left > 0:
            return ["same_pair", "decision_type", "opponent_type"]
        else:
            return []
    @staticmethod
    def error_message(player: Player, values):
        participant = player.participant
        if player.tries_left > 0:
            if participant.treatment == "human":
                answer_opponent = "human"
            else:
                answer_opponent = "robot"
        
            if not values["same_pair"] or values["decision_type"] != participant.game or values["opponent_type"] != answer_opponent:
                player.tries_left -= 1
                return "Not all answers are correct."
    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        participant = player.participant
        if player.tries_left == 0:
            participant.correct_answers = False
            return upcoming_apps[-1]
        else:
            participant.correct_answers = True
            return upcoming_apps[0]
page_sequence = [ControlQuestions]