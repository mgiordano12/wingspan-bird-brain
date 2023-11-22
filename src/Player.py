from Gamemat import Gamemat
from BirdCard import BirdCard
from BonusCard import BonusCard
import numpy as np
import names

class Player:
    #===================================================================================================================
    def __init__(self, birdcards: list, bonuscards: list, name = None):
        if name is None:
            # Low likelihood this could assign players the same name at random...
            self.name = names.get_first_name()
        else:
            self.name = name
        self.birdcards = []
        self.bonuscards = []
        self.food = {'Fish' : 1, 'Rodent' : 1, 'Fruit' : 1, 'Invertebrate' : 1, 'Seed' : 1}
        self.gamemat = Gamemat()
        self._assignStartingMaterials(birdcards,bonuscards)

    def _assignStartingMaterials(self, birdcards, bonuscards):
        # This makes it modular but is kinda annoying since you'll have to have to choose 
        # in this order.  TODO: Do we want different functions for initial choice of cards
        self.chooseBirdCards(birdcards)
        self.chooseBonusCards(bonuscards)
        # @owen interact with user to decide food as well
        assert np.sum(list(self.food.values())) + len(self.birdcards) == 5
        #TODO: Temporarily commented out since we don't have this functionality yet
        #assert len(self.bonuscards) == 1

    def chooseBirdCards(self, cards : list):
        if cards is not list:
            TypeError('If passing in cards to choose, must be a list')
        # @Owen: interact with user to decide the bird cards
        # FIXME:
        removedCards = cards[:2]
        # self.editBirdCards(removedCards, remove = True)
        return
    
    def chooseBonusCards(self, cards : list):
        if cards is not list:
            TypeError('If passing in cards to choose, must be a list')
        # @Owen: interact with user to decide the bonus cards

        # self.editBonusCards(removedCards, remove = True)
        return
    
    def editBirdCards(self, cards, remove = False):
        """
        Add bird cards to hand
        :param cards: Bird Cards to be added.  Can come in the form of a birdcard or list of birdcards
        :return: none
        """
        if (type(cards) is not BirdCard and type(cards) is not list) or (type(cards) is list and cards[0] is not BirdCard):
            TypeError('If passing in a card, must be of type BirdCard.')
        else:
            for card in cards:
                if remove:
                    if card not in self.birdcards:
                        raise Exception(f'{card} is already in the bird cards in this hand.')
                    self.birdcards.remove(card)
                else:
                    if card in self.birdcards:
                        raise Exception(f'{card} is not in this hand.')
                    self.birdcards.append(card)

    def editBonusCards(self, cards, remove = False):
        """
        Add bird cards to hand
        :param cards: Bonus Cards to be added.  Can come in the form of a bonuscard or list of bonuscards
        :return: none
        """
        if (type(cards) is not BonusCard and type(cards) is not list) or (type(cards) is list and cards[0] is not BonusCard):
            TypeError('If passing in a card, must be of type BonusCard.')
        else:
            for card in cards:
                if remove:
                    if card not in self.bonuscards:
                        raise Exception(f'{card} is not in the bonus cards in this hand.')
                    self.bonuscards.remove(card)
                else:
                    if card in self.bonuscards:
                        raise Exception(f'{card} is already in the bonus cards in this hand.')
                    self.bonuscards.append(card)

    def editFood(self, food : dict):
        """
        Add food to hand
        :param: Food to be added to this hand.  Must be in the form of a dictionary with food : amount
        :return: None
        """
        if type(food) is not dict:
            TypeError('Must pass food as dict')
        for food_type in food.keys():
            if food_type not in self.food.keys():
                TypeError(f'{food_type} is not a valid food type')
            if type(food_type[food]) is not int:
                TypeError(f'{food_type[food]} is not an integer')
            self.food[food_type] += food[food_type]



    def __repr__(self):
        return (f"Player Name: {self.name},\n"
                f"Bird Cards: {self.birdcards},\n"
                f"Bonus Cards: {self.bonuscards},\n\n"
                f"GameMat: \n{self.gamemat}\n\n"
                f"Food Tokens: {self.food}, Eggs: {self.gamemat.eggs}")
