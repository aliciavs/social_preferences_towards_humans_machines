
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'dictator'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 30
    SELF_X = (cu(330), cu(350), cu(390), cu(400), cu(450), cu(470), cu(510), cu(520), cu(440), cu(370), cu(600), cu(620), cu(660), cu(670), cu(720), cu(740), cu(780), cu(790), cu(710), cu(640), cu(870), cu(890), cu(930), cu(940), cu(990), cu(1010), cu(1050), cu(1060), cu(980), cu(910))
    SELF_Y = (cu(330), cu(310), cu(270), cu(260), cu(210), cu(190), cu(150), cu(140), cu(220), cu(290), cu(600), cu(580), cu(540), cu(530), cu(480), cu(460), cu(420), cu(410), cu(490), cu(560), cu(870), cu(850), cu(810), cu(800), cu(750), cu(730), cu(690), cu(680), cu(760), cu(830))
    OTHER_X = (cu(680), cu(680), cu(1050), cu(690), cu(1020), cu(730), cu(810), cu(870), cu(710), cu(680), cu(410), cu(410), cu(780), cu(420), cu(750), cu(460), cu(540), cu(600), cu(440), cu(410), cu(140), cu(140), cu(510), cu(150), cu(480), cu(190), cu(270), cu(330), cu(170), cu(140))
    OTHER_Y = (cu(1060), cu(1060), cu(690), cu(1050), cu(720), cu(1010), cu(930), cu(870), cu(1030), cu(1060), cu(790), cu(790), cu(420), cu(780), cu(450), cu(740), cu(660), cu(600), cu(760), cu(790), cu(520), cu(520), cu(150), cu(510), cu(180), cu(470), cu(390), cu(330), cu(490), cu(520))
class Subsession(BaseSubsession):
    self_x = models.CurrencyField()
    self_y = models.CurrencyField()
    other_x = models.CurrencyField()
    other_y = models.CurrencyField()
def creating_session(subsession: Subsession):
    session = subsession.session
    import random
    random.seed(1111)
    order = list(range(30))
    random.shuffle(order)
    subsession.self_x = C.SELF_X[order[subsession.round_number - 1]]
    subsession.self_y = C.SELF_Y[order[subsession.round_number - 1]]
    subsession.other_x = C.OTHER_X[order[subsession.round_number - 1]]
    subsession.other_y = C.OTHER_Y[order[subsession.round_number - 1]]
class Group(BaseGroup):
    pass
class Player(BasePlayer):
    payoff_round = models.IntegerField()
    decision = models.StringField()
    treatment = models.StringField()
class Decision(Page):
    form_model = 'player'
    form_fields = ['decision']
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            progress=100*player.round_number/C.NUM_ROUNDS,
        )
    @staticmethod
    def js_vars(player: Player):
        session = player.session
        subsession = player.subsession
        return dict(
            self_x=int(subsession.self_x),
            self_y=int(subsession.self_y),
            other_x=int(subsession.other_x),
            other_y=int(subsession.other_y),
        )
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        session = player.session
        subsession = player.subsession
        participant = player.participant
        import random
        player.treatment = participant.treatment
        if player.round_number == C.NUM_ROUNDS:
            player.payoff_round = random.randint(1,C.NUM_ROUNDS)
            subsession_payoffround = subsession.in_round(player.payoff_round)
            player_payoffround = player.in_round(player.payoff_round)
            if player_payoffround.decision == "X":
                player.payoff = subsession_payoffround.self_x
            else:
                player.payoff = subsession_payoffround.self_y
class Results(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS
    @staticmethod
    def vars_for_template(player: Player):
        session = player.session
        subsession = player.subsession
        subsession_payoffround = subsession.in_round(player.payoff_round)
        player_payoffround = player.in_round(player.payoff_round)
        return dict(
            self_x=subsession_payoffround.self_x,
            self_y=subsession_payoffround.self_y,
            other_x=subsession_payoffround.other_x,
            other_y=subsession_payoffround.other_y,
            decision=player_payoffround.decision
        )
page_sequence = [Decision, Results]