from os import environ
SESSION_CONFIG_DEFAULTS = dict(real_world_currency_per_point=0.002, participation_fee=1)
SESSION_CONFIGS = [dict(name='dictator_human', num_demo_participants=1, app_sequence=['introduction', 'dictator_instructions', 'control_questions', 'dictator', 'final_results', 'survey', 'final_screen'], treatments_human=True, treatments_robot=False, use_browser_bots=False), dict(name='dictator_robot', num_demo_participants=10, app_sequence=['introduction', 'dictator_instructions', 'control_questions', 'dictator', 'final_results', 'survey', 'final_screen'], treatments_human=False, treatments_robot=True, use_browser_bots=False), dict(name='trust_human', num_demo_participants=8, app_sequence=['introduction', 'trust_instructions', 'control_questions', 'trust_human_firstmover', 'trust_human_secondmover', 'trust_human_match', 'final_results', 'survey', 'final_screen'], treatments_human=True, treatments_robot=False, use_browser_bots=False), dict(name='trust_robot_secondmover', num_demo_participants=5, app_sequence=['introduction', 'trust_instructions', 'control_questions', 'trust_robot_secondmover', 'final_results', 'survey', 'final_screen'], treatments_human=False, treatments_robot=True, test=False, use_browser_bots=False)]
LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'GBP'
USE_POINTS = True
DEMO_PAGE_INTRO_HTML = ''
PARTICIPANT_FIELDS = ['treatment', 'game', 'correct_answers', 'role', 'decisions']
SESSION_FIELDS = []
ROOMS = [dict(name='Test', display_name='Test'), dict(name='Prolific', display_name='Prolific')]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

SECRET_KEY = 'blahblah'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']


