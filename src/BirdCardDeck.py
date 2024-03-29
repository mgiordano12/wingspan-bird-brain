from BirdCard import BirdCard
from load_data_functions import load_birdcards
import random

class BirdCardDeck:
    #===================================================================================================================
    def __init__(self, expansions = None, seed=0):
        if seed != 0:
            random.seed(seed)
        self.facedown_cards = load_birdcards() # load the deck of all cards
        self.discarded = set() # no cards have been discarded yet
        self.faceup_cards = [None, None, None] # initialize faceup cards
        self.refill_faceup_cards()

    #===================================================================================================================
    def refill_faceup_cards(self):
        n = sum([1 for i in self.faceup_cards if i is None])
        new_cards = random.sample(self.facedown_cards, n) # new faceup cards
        for i in new_cards: # remove new cards from the facedown cards
            self.facedown_cards.remove(i)
        self.faceup_cards += new_cards # add the cards to the faceup cards
        self.faceup_cards = [i for i in self.faceup_cards if i is not None] # remove None faceup cards
        assert len(self.faceup_cards) == 3

    #===================================================================================================================
    def draw_faceup_card(self, i):
        card = self.faceup_cards[i]
        self.faceup_cards[i] = None # remove the card
        return card

    #===================================================================================================================
    def draw_facedown_cards(self, n = 1):
        if n > len(self.facedown_cards):
            raise StopIteration
        cards = []
        for i in range(n):
            card = random.sample(self.facedown_cards, 1)[0]
            cards.append(card)
            self.facedown_cards.remove(card) # remove the card
        if n == 1:
            return cards[0]
        else:
            return cards
    
    #===================================================================================================================
    def discard(self, card):
        if type(card) is not BirdCard:
            raise TypeError('Discard must be a BirdCard.')
        elif card in self.discarded:
            raise Exception(f'{card} has already been discarded.')
        self.discarded.add(card)

    #===================================================================================================================
    # This only displays the bird tray
    def __repr__(self):
        return f"{self.faceup_cards}"
    
    # Allow for iteration
    def __iter__(self):
        return self

    # FIXME: Should draw facedown cards just be implemented here?
    def __next__(self):
        return self.draw_facedown_cards()
    
    def __len__(self):
        return len(self.facedown_cards)