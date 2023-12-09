from Power import Power
from Player import Player
from Gameplay_Constants import *

class PowerEggsForFood(Power):
    def __init__(self,food_type,amount):
        assert food_type in FOOD_TYPES
        self.food_type = food_type
        self.amount = amount

    def performpower(self, player : Player):
        # Note: Choosing where the egg is taken from and what type of food is gained is handled by these funcs
        player.getGameMat().editeggs() # TODO: this may need some refactoring.  Where and how do we decide what eggs to remove
        player.editFood({self.food_type : self.amount})