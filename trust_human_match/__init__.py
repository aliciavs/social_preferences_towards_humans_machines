
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'trust_human_match'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    NUM_ROUNDS_MAIN = 30
    SELF_X = (cu(330), cu(350), cu(370), cu(390), cu(400), cu(440), cu(450), cu(470), cu(510), cu(520), cu(600), cu(620), cu(640), cu(660), cu(670), cu(710), cu(720), cu(740), cu(780), cu(790), cu(870), cu(890), cu(910), cu(930), cu(940), cu(980), cu(990), cu(1010), cu(1050), cu(1060))
    SELF_Y = (cu(330), cu(310), cu(290), cu(270), cu(260), cu(220), cu(210), cu(190), cu(150), cu(140), cu(600), cu(580), cu(560), cu(540), cu(530), cu(490), cu(480), cu(460), cu(420), cu(410), cu(870), cu(850), cu(830), cu(810), cu(800), cu(760), cu(750), cu(730), cu(690), cu(680))
    SELF_Z_WEL = (cu(190), cu(170), cu(150), cu(130), cu(120), cu(80), cu(70), cu(50), cu(10), cu(0), cu(460), cu(440), cu(420), cu(400), cu(390), cu(350), cu(340), cu(320), cu(280), cu(270), cu(730), cu(710), cu(690), cu(670), cu(660), cu(620), cu(610), cu(590), cu(550), cu(540))
    SELF_Z_MIS = (cu(470), cu(490), cu(510), cu(530), cu(540), cu(580), cu(590), cu(610), cu(650), cu(660), cu(740), cu(760), cu(780), cu(800), cu(810), cu(850), cu(860), cu(880), cu(920), cu(930), cu(1010), cu(1030), cu(1050), cu(1070), cu(1080), cu(1120), cu(1130), cu(1150), cu(1190), cu(1200))
    OTHER_X = (cu(680), cu(680), cu(680), cu(1050), cu(690), cu(710), cu(1020), cu(730), cu(810), cu(870), cu(410), cu(410), cu(410), cu(780), cu(420), cu(440), cu(750), cu(460), cu(540), cu(600), cu(140), cu(140), cu(140), cu(510), cu(150), cu(170), cu(480), cu(190), cu(270), cu(330))
    OTHER_Y = (cu(1060), cu(1060), cu(1060), cu(690), cu(1050), cu(1030), cu(720), cu(1010), cu(930), cu(870), cu(790), cu(790), cu(790), cu(420), cu(780), cu(760), cu(450), cu(740), cu(660), cu(600), cu(520), cu(520), cu(520), cu(150), cu(510), cu(490), cu(180), cu(470), cu(390), cu(330))
    OTHER_Z_WEL = (cu(1200), cu(1200), cu(1200), cu(830), cu(1190), cu(1170), cu(860), cu(1150), cu(1070), cu(1010), cu(930), cu(930), cu(930), cu(560), cu(920), cu(900), cu(590), cu(880), cu(800), cu(740), cu(660), cu(660), cu(660), cu(290), cu(650), cu(630), cu(320), cu(610), cu(530), cu(470))
    OTHER_Z_MIS = (cu(540), cu(540), cu(540), cu(910), cu(550), cu(570), cu(880), cu(590), cu(670), cu(730), cu(270), cu(270), cu(270), cu(640), cu(280), cu(300), cu(610), cu(320), cu(400), cu(460), cu(0), cu(0), cu(0), cu(370), cu(10), cu(30), cu(340), cu(50), cu(130), cu(190))
    BONUS = cu(200)
class Subsession(BaseSubsession):
    pass
def group_by_arrival_time_method(subsession: Subsession, waiting_players):
    first_movers1 = [p for p in waiting_players if p.participant.role == "first1"]
    first_movers2 = [p for p in waiting_players if p.participant.role == "first2"]
    second_movers1 = [p for p in waiting_players if p.participant.role == "second1"]
    second_movers2 = [p for p in waiting_players if p.participant.role == "second2"]
    
    if len(second_movers1)>0 and len(first_movers1)>0:
        return [second_movers1[0], first_movers1[0]]
    if len(second_movers2)>0 and len(first_movers2)>0:
        return [second_movers2[0], first_movers2[0]]
class Group(BaseGroup):
    payoff_round = models.IntegerField()
    trust = models.BooleanField()
    decision = models.StringField()
    belief_decision = models.StringField()
    misbehaved = models.BooleanField()
    self_x = models.CurrencyField()
    self_y = models.CurrencyField()
    self_z_wel = models.CurrencyField()
    self_z_mis = models.CurrencyField()
    other_x = models.CurrencyField()
    other_y = models.CurrencyField()
    other_z_wel = models.CurrencyField()
    other_z_mis = models.CurrencyField()
def set_payoffs(group: Group):
    import random
    group.payoff_round = random.randint(1,C.NUM_ROUNDS)
    
    random.seed(1111)
    order = list(range(30))
    random.shuffle(order)
    
    group.self_x = C.SELF_X[order[group.payoff_round - 1]]
    group.self_y = C.SELF_Y[order[group.payoff_round - 1]]
    group.self_z_wel = C.SELF_Z_WEL[order[group.payoff_round - 1]]
    group.self_z_mis = C.SELF_Z_MIS[order[group.payoff_round - 1]]
    group.other_x = C.OTHER_X[order[group.payoff_round - 1]]
    group.other_y = C.OTHER_Y[order[group.payoff_round - 1]]
    group.other_z_wel = C.OTHER_Z_WEL[order[group.payoff_round - 1]]
    group.other_z_mis = C.OTHER_Z_MIS[order[group.payoff_round - 1]]
    
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    group.trust = p2.participant.decisions["trust" + str(group.payoff_round)]
    group.belief_decision = p2.participant.decisions["belief" + str(group.payoff_round)]
    group.decision = p1.participant.decisions["decision" + str(group.payoff_round)]
    group.misbehaved = p2.participant.decisions["misbehaved" + str(group.payoff_round)]
    
    if not group.trust:
        if group.misbehaved:
            p1.payoff = group.self_z_mis
            p2.payoff = group.other_z_mis
        else:
            p1.payoff = group.self_z_wel
            p2.payoff = group.other_z_wel
    else:
        if group.decision == "X":
            p1.payoff = group.self_x
            p2.payoff = group.other_x
        else:
            p1.payoff = group.self_y
            p2.payoff = group.other_y
    p1.payoff_from_option = p1.payoff
    p2.payoff_from_option = p2.payoff
    p2.payoff += (group.decision == group.belief_decision) * C.BONUS
class Player(BasePlayer):
    payoff_from_option = models.CurrencyField()
    treatment = models.StringField(initial='human')
class GroupWaitPage(WaitPage):
    group_by_arrival_time = True
    after_all_players_arrive = set_payoffs
class Results(Page):
    form_model = 'group'
page_sequence = [GroupWaitPage, Results]