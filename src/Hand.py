from BirdCard import BirdCard
from BonusCard import BonusCard

class Hand:
    #===================================================================================================================
    def __init__(self, birdcards=[], bonuscards=[], food={'Fish':0, 'Rodent':0, 'Fruit':0, 'Invertebrate':0, 'Seed':0,}):
        self.birdcards = birdcards
        self.bonuscards = bonuscards
        self.food = food

    #===================================================================================================================
    def add(self, a, n=0):
        if type(a) is BirdCard:
            if a in self.birdcards:
                raise Exception(f'{a} is already in the bird cards in this hand.')
            else:
                self.birdcards.append(a)
        elif type(a) is BonusCard:
            if a in self.bonuscards:
                raise Exception(f'{a} is already in the bonus cards in this hand.')
            else:
                self.bonuscards.append(a)
        elif type(a) is str:
            if a not in self.food.keys():
                raise KeyError(f'{a} is not a valid food type.')
            elif type(n) is not int:
                raise TypeError('n must be an integer.')
            elif n <= 0:
                raise ValueError('n must be > 0 to add food to this hand.')
            else:
                self.food[a] += n
        else:
            raise TypeError('If passing in a card, must be of type BirdCard or BonusCard. If passing in a string, must be a valid food type.')
        
    #===================================================================================================================
    def remove(self, a, n=0):
        if type(a) is BirdCard:
            if a not in self.birdcards:
                raise Exception(f'{a} is not in the bird cards in this hand.')
            else:
                self.birdcards.remove(a)
        elif type(a) is BonusCard:
            if a not in self.bonuscards:
                raise Exception(f'{a} is not in the bonus cards in this hand.')
            else:
                self.bonuscards.remove(a)
        elif type(a) is str:
            if a not in self.food.keys():
                raise KeyError(f'{a} is not a valid food type.')
            elif type(n) is not int:
                raise TypeError('n must be an integer.')
            elif n <= 0:
                raise ValueError('n must be >= 0 to remove food from this hand.')
            elif self.food[a] < n:
                raise Exception(f'Cannot remove {n} {a} foods. Only {self.food[a]} foods in this hand.')
            else:
                self.food[a] -= n
        else:
            raise TypeError('If passing in a card, must be of type BirdCard or BonusCard. If passing in a string, must be a valid food type.')