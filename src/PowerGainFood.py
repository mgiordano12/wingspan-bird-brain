from Power import Power
from Player import Player
from Gameplay_Constants import *

class PowerGainFood(Power):
    def __init__(self,food_type,amount):
        assert food_type in BIRDFEEDER_FACES
        self.food_type = food_type
        self.amount = amount

    def performpower(self, player : Player):
        player.editFood({self.food_type : self.amount})