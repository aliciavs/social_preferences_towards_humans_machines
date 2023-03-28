import survey as pages
from . import *
c = cu

class PlayerBot(Bot):
    def play_round(self):
        genders = ["female", "male", "other"]
        fields_of_study = ["na", "econ", "law", "psych", "politics", "med", "natural", "engineer", "other_social", "other"]
        employments = ["no", "part", "full"]

        yield Survey, dict(
            what_happens_with_payoffs="xyz",
            age=25,
            gender=genders[self.player.id_in_group%3],
            degree=self.player.id_in_group%5,
            field_of_study=fields_of_study[self.player.id_in_group%10],
            employment=employments[self.player.id_in_group%3],
            familiarity=self.player.id_in_group%5,
            confidence=self.player.id_in_group%5,
            redistribution=self.player.id_in_group%5,
        )