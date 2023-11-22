import EndOfRoundGoal
from load_data_functions import *
import random

class EndOfRoundGoalMat:
    #===================================================================================================================
    def __init__(self, deck_names = ['originalcore'], seed=0):
        if seed != 0:
            random.seed(seed)
        loaded_goals = load_endofroundgoals(deck_names = deck_names)
        self.goals = random.sample(loaded_goals, 4)

    #===================================================================================================================
    def __repr__(self):
        return f"Goals: {self.goals}"