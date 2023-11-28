from BirdfeederDie import BirdfeederDie

class Birdfeeder:

    def __init__(self):
        # TODO: We need to randomly seed the birdfeeder, which isn't trivial
        self.food = list() # initialize
        self.reroll() # roll for 1st time

    def reroll(self):
        if len(set(self.food)) > 1:
            raise Exception(f'Cannot reroll feeder if there is more than 1 type of food in it. Currently has {self.food}.')
        
        del self.food # clear the birdfeeder
        self.food = [
            BirdfeederDie().faceup_side, BirdfeederDie().faceup_side, BirdfeederDie().faceup_side, 
            BirdfeederDie().faceup_side, BirdfeederDie().faceup_side
        ]

    def take(self, food):
        if food not in self.food:
            raise ValueError(f'{food} is not in the birdfeeder.')
        self.food.remove(food)

    def __repr__(self):
        return f'Birdfeeder: {self.food}'
