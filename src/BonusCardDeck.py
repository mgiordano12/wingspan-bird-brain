from BonusCard import BonusCard
from load_data_functions import load_bonuses
import random

class BonusCardDeck:
    #===================================================================================================================
    def __init__(self):
        self.deck = load_bonuses()
        self.discarded = set()

    #===================================================================================================================
    def draw_card(self):
        card = random.sample(self.deck, 1)[0] # draw card
        self.deck.remove(card) # remove card from deck
        return card
    
    #===================================================================================================================
    def discard(self, card):
        if type(card) is not BonusCard:
            raise TypeError(f'Discard must be a BonusCard.')
        elif card in self.discarded:
            raise Exception(f'{card} has already been discarded.')
        self.discarded.add(card)