from BirdfeederDie import BirdfeederDie
import random
from Gameplay_Constants import *
import numpy as np

BUFFER_MULTIPLIER = 10
MAX_DIE_IN_BIRDFEEDER = 5

class Birdfeeder:
    def __init__(self,seed=0):
        self.food = list() # initialize
        if seed != 0:
            self.seeded = True
            # Produce food list that is bigger than we could reasonably go through in a game
            self.food_destiny = [BirdfeederDie(seed = random.randint(1,100000)).faceup_side\
                                 for _ in range(np.sum(NUMBER_OF_TURNS)*NUMBER_OF_ROUNDS*MAX_NUMBER_OF_PLAYERS*BUFFER_MULTIPLIER)]
            self.num_rerolls = 0
        else:
            self.seeded = False

        self.roll() # roll for 1st time

    def roll(self):
        if len(set(self.food)) > 1:
            raise Exception(f'Cannot reroll feeder if there is more than 1 type of food in it. Currently has {self.food}.')
        del self.food # clear the birdfeeder
        if self.seeded:
            # Seeding is implemented such that every re-roll is identical
            self.food = [self.food_destiny[self.num_rerolls*MAX_DIE_IN_BIRDFEEDER+ind] for ind in range(MAX_DIE_IN_BIRDFEEDER)]
            self.num_rerolls += 1
        else:
            self.food = [BirdfeederDie().faceup_side for _ in range(MAX_DIE_IN_BIRDFEEDER)]

    def take(self, food):
        if food not in self.food:
            raise ValueError(f'{food} is not in the birdfeeder.')
        self.food.remove(food)

    def __repr__(self):
        return f'Birdfeeder: {self.food}'
