import random
from Gameplay_Constants import *

class BirdfeederDie:
    def __init__(self, seed = 0):
        if seed != 0:
            random.seed(seed)
        self.faces = BIRDFEEDER_FACES
        self.roll()
    
    def roll(self):
        self.faceup_side = random.sample(self.faces, 1)[0]

    def __repr__(self):
        return f'BirdfeederDie: {self.faceup_side}'