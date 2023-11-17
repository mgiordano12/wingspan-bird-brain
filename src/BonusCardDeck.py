from BonusCard import BonusCard
from load_data_functions import load_bonuses
import random

class BonusCardDeck:
    #===================================================================================================================
    def __init__(self):
        self.deck = load_bonuses()
        self.discarded = set()

    #===================================================================================================================
    def draw_cards(self, n = 1):
        cards = []
        for i in range(n):
            card = random.sample(self.deck, 1)[0] # draw card
            cards.append(card)
            self.deck.remove(card) # remove card from deck
        if n == 1:
            return cards[0]
        else:
            return cards
    
    #===================================================================================================================
    def discard(self, card):
        if type(card) is not BonusCard:
            raise TypeError(f'Discard must be a BonusCard.')
        elif card in self.discarded:
            raise Exception(f'{card} has already been discarded.')
        self.discarded.add(card)