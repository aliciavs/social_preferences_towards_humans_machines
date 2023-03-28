
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    pass
class Player(BasePlayer):
    what_happens_with_payoffs = models.LongStringField(label='Please briefly describe what you think exactly happens to the payoffs earned by the other participant.')
    age = models.IntegerField(label='How old are you?', max=100, min=18)
    gender = models.StringField(choices=[['female', 'female'], ['male', 'male'], ['other', 'other/non-binary']], label='What is your gender?', widget=widgets.RadioSelect)
    degree = models.IntegerField(choices=[[0, 'No degree'], [1, 'High school'], [2, 'Bachelor'], [3, 'Master'], [4, 'PhD']], label='What is your highest educational degree?', widget=widgets.RadioSelect)
    field_of_study = models.StringField(choices=[['na', 'Not applicable'], ['econ', 'Economics'], ['law', 'Law'], ['psych', 'Psychology'], ['politics', 'Political sciences'], ['med', 'Medicine'], ['natural', 'Natural sciences'], ['engineer', 'Engineering'], ['other_social', 'Other social sciences'], ['other', 'Other']], label='If you go/went to university, what is/was your major?', widget=widgets.RadioSelect)
    employment = models.StringField(choices=[['no', 'Unemployed'], ['part', 'Part-time'], ['full', 'Full-time']], label='What is your employment status?', widget=widgets.RadioSelect)
    familiarity = models.IntegerField(choices=[[0, 'Not familiar at all'], [1, 'Rather not familiar'], [2, 'Neutral'], [3, 'A little familiar'], [4, 'Very familiar']], label='How familiar are you with new technologies such as machine learning?', widget=widgets.RadioSelect)
    confidence = models.IntegerField(choices=[[0, 'No confidence at all'], [1, 'Rather no confidence'], [2, 'Neutral'], [3, 'Little confidence'], [4, 'Strong confidence']], label='How much confidence do you have in new technologies such as machine learning?', widget=widgets.RadioSelect)
    redistribution = models.IntegerField(choices=[[0, 'Redistribution should be decreased a lot.'], [1, 'Redistribution should be decreased a little.'], [2, 'The current redistribution levels should be maintained.'], [3, 'Redistribution should be increased a little.'], [4, 'Redistribution should be increased a lot.']], label='Do you think the government should increase or decrease income redistribution?', widget=widgets.RadioSelect)
class Survey(Page):
    form_model = 'player'
    form_fields = ['what_happens_with_payoffs', 'age', 'gender', 'degree', 'field_of_study', 'employment', 'familiarity', 'confidence', 'redistribution']
page_sequence = [Survey]