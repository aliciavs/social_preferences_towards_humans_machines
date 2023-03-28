
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'trust_robot_secondmover'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 30
    SELF_X = (cu(330), cu(350), cu(370), cu(390), cu(400), cu(440), cu(450), cu(470), cu(510), cu(520), cu(600), cu(620), cu(640), cu(660), cu(670), cu(710), cu(720), cu(740), cu(780), cu(790), cu(870), cu(890), cu(910), cu(930), cu(940), cu(980), cu(990), cu(1010), cu(1050), cu(1060))
    SELF_Y = (cu(330), cu(310), cu(290), cu(270), cu(260), cu(220), cu(210), cu(190), cu(150), cu(140), cu(600), cu(580), cu(560), cu(540), cu(530), cu(490), cu(480), cu(460), cu(420), cu(410), cu(870), cu(850), cu(830), cu(810), cu(800), cu(760), cu(750), cu(730), cu(690), cu(680))
    SELF_Z_WEL = (cu(190), cu(170), cu(150), cu(130), cu(120), cu(80), cu(70), cu(50), cu(10), cu(0), cu(460), cu(440), cu(420), cu(400), cu(390), cu(350), cu(340), cu(320), cu(280), cu(270), cu(730), cu(710), cu(690), cu(670), cu(660), cu(620), cu(610), cu(590), cu(550), cu(540))
    SELF_Z_MIS = (cu(470), cu(490), cu(510), cu(530), cu(540), cu(580), cu(590), cu(610), cu(650), cu(660), cu(740), cu(760), cu(780), cu(800), cu(810), cu(850), cu(860), cu(880), cu(920), cu(930), cu(1010), cu(1030), cu(1050), cu(1070), cu(1080), cu(1120), cu(1130), cu(1150), cu(1190), cu(1200))
    OTHER_X = (cu(680), cu(680), cu(680), cu(1050), cu(690), cu(710), cu(1020), cu(730), cu(810), cu(870), cu(410), cu(410), cu(410), cu(780), cu(420), cu(440), cu(750), cu(460), cu(540), cu(600), cu(140), cu(140), cu(140), cu(510), cu(150), cu(170), cu(480), cu(190), cu(270), cu(330))
    OTHER_Y = (cu(1060), cu(1060), cu(1060), cu(690), cu(1050), cu(1030), cu(720), cu(1010), cu(930), cu(870), cu(790), cu(790), cu(790), cu(420), cu(780), cu(760), cu(450), cu(740), cu(660), cu(600), cu(520), cu(520), cu(520), cu(150), cu(510), cu(490), cu(180), cu(470), cu(390), cu(330))
    OTHER_Z_WEL = (cu(1200), cu(1200), cu(1200), cu(830), cu(1190), cu(1170), cu(860), cu(1150), cu(1070), cu(1010), cu(930), cu(930), cu(930), cu(560), cu(920), cu(900), cu(590), cu(880), cu(800), cu(740), cu(660), cu(660), cu(660), cu(290), cu(650), cu(630), cu(320), cu(610), cu(530), cu(470))
    OTHER_Z_MIS = (cu(540), cu(540), cu(540), cu(910), cu(550), cu(570), cu(880), cu(590), cu(670), cu(730), cu(270), cu(270), cu(270), cu(640), cu(280), cu(300), cu(610), cu(320), cu(400), cu(460), cu(0), cu(0), cu(0), cu(370), cu(10), cu(30), cu(340), cu(50), cu(130), cu(190))
class Subsession(BaseSubsession):
    self_x = models.CurrencyField()
    self_y = models.CurrencyField()
    self_z_wel = models.CurrencyField()
    self_z_mis = models.CurrencyField()
    other_x = models.CurrencyField()
    other_y = models.CurrencyField()
    other_z_wel = models.CurrencyField()
    other_z_mis = models.CurrencyField()
def creating_session(subsession: Subsession):
    session = subsession.session
    import random
    random.seed(1111)
    order = list(range(30))
    random.shuffle(order)
    subsession.self_x = C.SELF_X[order[subsession.round_number - 1]]
    subsession.self_y = C.SELF_Y[order[subsession.round_number - 1]]
    subsession.self_z_wel = C.SELF_Z_WEL[order[subsession.round_number - 1]]
    subsession.self_z_mis = C.SELF_Z_MIS[order[subsession.round_number - 1]]
    subsession.other_x = C.OTHER_X[order[subsession.round_number - 1]]
    subsession.other_y = C.OTHER_Y[order[subsession.round_number - 1]]
    subsession.other_z_wel = C.OTHER_Z_WEL[order[subsession.round_number - 1]]
    subsession.other_z_mis = C.OTHER_Z_MIS[order[subsession.round_number - 1]]
    
    if session.config['test']:
        for p in subsession.get_players():
            random.seed(p.id_in_group*subsession.round_number*123)
            p.trust_wel = bool(random.getrandbits(1))
            p.trust_mis = bool(random.getrandbits(1))
    else:
        import pandas as pd
        data_wel = pd.read_csv("trust_robot_secondmover/predictions_trust_first_wel.csv")
        data_mis = pd.read_csv("trust_robot_secondmover/predictions_trust_first_mis.csv")
        for p in subsession.get_players():
            prediction_wel = data_wel.loc[p.id_in_group - 1]
            prediction_mis = data_mis.loc[p.id_in_group - 1]
            p.trust_wel = bool(prediction_wel[order[subsession.round_number - 1]])
            p.trust_mis = bool(prediction_mis[order[subsession.round_number - 1]])
    
    for p in subsession.get_players():
        if order[subsession.round_number - 1] % 2:
            p.misbehaved = p.participant.id_in_session % 2
        else:
            p.misbehaved = 1 - p.participant.id_in_session % 2
class Group(BaseGroup):
    pass
class Player(BasePlayer):
    payoff_round = models.IntegerField()
    trust_wel = models.BooleanField()
    trust_mis = models.BooleanField()
    decision = models.StringField()
    treatment = models.StringField()
    misbehaved = models.BooleanField()
class Decision(Page):
    form_model = 'player'
    form_fields = ['decision']
    @staticmethod
    def vars_for_template(player: Player):
        session = player.session
        subsession = player.subsession
        if player.misbehaved:
            self_z = subsession.self_z_mis
            other_z = subsession.other_z_mis
        else:
            self_z = subsession.self_z_wel
            other_z = subsession.other_z_wel
        return dict(
            progress=100*player.round_number/C.NUM_ROUNDS,
            self_z=self_z,
            other_z=other_z
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
            if player_payoffround.misbehaved:
                trust = player_payoffround.trust_mis
            else:
                trust = player_payoffround.trust_wel
            if not trust:
                if player_payoffround.misbehaved:
                    player.payoff = subsession_payoffround.self_z_mis
                else:
                    player.payoff = subsession_payoffround.self_z_wel
            else:
                if player_payoffround.decision == "X":
                    player.payoff = subsession_payoffround.self_x
                else:
                    player.payoff = subsession_payoffround.self_y
class Results(Page):
    form_model = 'group'
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS
    @staticmethod
    def vars_for_template(player: Player):
        session = player.session
        subsession = player.subsession
        subsession_payoffround = subsession.in_round(player.payoff_round)
        player_payoffround = player.in_round(player.payoff_round)
        if player_payoffround.misbehaved:
            trust = player_payoffround.trust_mis
        else:
            trust = player_payoffround.trust_wel
        return dict(
            self_x=subsession_payoffround.self_x,
            self_y=subsession_payoffround.self_y,
            self_z_wel=subsession_payoffround.self_z_wel,
            self_z_mis=subsession_payoffround.self_z_mis,
            other_x=subsession_payoffround.other_x,
            other_y=subsession_payoffround.other_y,
            other_z_wel=subsession_payoffround.other_z_wel,
            other_z_mis=subsession_payoffround.other_z_mis,
            trust=trust,
            decision=player_payoffround.decision,
            misbehaved=player_payoffround.misbehaved
        )
page_sequence = [Decision, Results]