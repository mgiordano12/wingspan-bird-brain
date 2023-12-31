import random

class BirdfeederDie:
    def __init__(self):
        self.faces = ['Fish', 'Rodent', 'Fruit', 'Invertebrate', 'Seed', 'Invertebrate+Seed',]
        self.roll()
    
    def roll(self):
        self.faceup_side = random.sample(self.faces, 1)[0]

    def __repr__(self):
        return f'BirdfeederDie: {self.faceup_side}'