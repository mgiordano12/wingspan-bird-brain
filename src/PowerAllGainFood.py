from Power import Power
from Player import Player
from Gameplay_Constants import *

class PowerAllGainFood(Power):
    def __init__(self,food_type,amount):
        assert food_type in FOOD_TYPES
        self.food_type = food_type
        self.amount = amount

    def performpower(self, players : list):
        for player in players:
            # Note: Choosing what type of food is gained if it's wild is handled in this func 
            player.editFood({self.food_type : self.amount})