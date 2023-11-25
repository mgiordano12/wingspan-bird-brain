from BirdfeederDie import BirdfeederDie

class Birdfeeder:

    def __init__(self):
        # TODO: We need to randomly seed the birdfeeder, which isn't trivial
        self.food = list()
        self.can_be_rerolled = True
        self.reroll() # roll for 1st time

    def reroll(self):
        # if not self.can_be_rerolled:
        #     raise Exception(f'Bird feeder cannot be re-rolled. Currently has {self.food}.')
        
        del self.food # clear the birdfeeder
        self.food = [
            BirdfeederDie().faceup_side, BirdfeederDie().faceup_side, 
            BirdfeederDie().faceup_side, BirdfeederDie().faceup_side, 
            BirdfeederDie().faceup_side
        ]
        self.can_be_rerolled = False

    def take(self, food):
        if food not in self.food:
            raise ValueError(f'{food} is not in the birdfeeder. Birdfeeder has {self.food}')
        
        self.food.remove(food)

        if len(set(self.food)) <= 1:
            self.can_be_rerolled = True

    def __repr__(self):
        return f'Birdfeeder: {self.food}'