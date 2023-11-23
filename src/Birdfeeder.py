from BirdfeederDie import BirdfeederDie

class Birdfeeder:

    def __init__(self):
        self.in_feeder = list()
        self.out_of_feeder = list()
        self.can_be_rerolled = True
        self.roll() # roll for 1st time

    def roll(self):
        if not self.can_be_rerolled:
            raise Exception(f'Bird feeder cannot be re-rolled. Currently has {self.in_feeder}.')
        
        self.in_feeder, self.out_of_feeder = list(), list()
        self.in_feeder = [
            BirdfeederDie().faceup_side, BirdfeederDie().faceup_side, 
            BirdfeederDie().faceup_side, BirdfeederDie().faceup_side, 
            BirdfeederDie().faceup_side
        ]
        self.can_be_rerolled = False

    def take(self, food):
        if food not in self.in_feeder:
            raise ValueError(f'{food} is not in the birdfeeder.')

        if len(set(food)) <= 1:
            self.can_be_rerolled = True
        
        self.in_feeder.remove(food)
        self.out_of_feeder.append(food)