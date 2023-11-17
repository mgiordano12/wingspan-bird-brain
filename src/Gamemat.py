from BirdCard import BirdCard
from Habitat import Habitat

class Gamemat:
    #===========================================================================
    def __init__(self):
        self.habitats = {'forest' : list(), 'grassland' : list(), 'wetland' : list()}
        self.eggs = 0

    #===========================================================================
    def playcard(self, card, habitat):
        if type(habitat) is not str or habitat not in self.habitats.keys():
            raise Exception('Habitat must be a string in ["forest", "grassland", "wetland"].')
        elif type(card) is not BirdCard:
            raise TypeError('Card must of type BirdCard.')
        elif len(self.__dict__[habitat]) == 5:
            raise Exception(f'{habitat} already has 5 cards in it.')
        elif card.__dict__[habitat] is not True:
            raise Exception(f'{card} can not be played in {habitat}. It is not a valid habitat for this bird.')

        egg_cost = 0
        if len(self.habitats[habitat] > 0) and len(self.habitats[habitat] < 3):
            # .... The cards which take up multiple spaces are gonna break this.  Might consider using
            # a habitat class.  I started building one.  Not sure if it's worth it
            egg_cost = 1
        elif len(self.habitats[habitat]) < 5:
            egg_cost = 2
        #### TODO: @owen Go to GUI and choose eggs to remove
        #self.editeggs(returnedCard, n)

    #===========================================================================
    def findcard(self, card):
        if card not in self.forest + self.grassland + self.wetland:
            raise Exception(f'{card} is not in play on this mat.')
        
        # Figure out which habitat the bird is in.
        if card in self.forest:
            hab = 'forest'
        elif card in self.grassland:
            hab = 'grassland'
        elif card in self.wetland:
            hab = 'wetland'

        # Find the index the bird is at
        idx = [i for i,c in enumerate(self.__dict__[hab]) if c==card][0]

        return hab, idx


    #===========================================================================
    def tuckcard(self, card):
        if type(card) is not BirdCard:
            raise TypeError('Card must be of type BirdCard.')
        
        # Find the card
        hab, idx = self.findcard(card)

        # Add a tucked card to the bird
        """
        THINK: Should we add the tucked cards to the discarded cards
        To keep track of them and so that they're no longer in play
        """
        self.__dict__[hab][idx].tuckedcards += 1
    
    #===========================================================================
    def cachefood(self, card):
        if type(card) is not BirdCard:
            raise TypeError('Card must be of type BirdCard.')
        
        # Find the card
        hab, idx = self.findcard(card)

        # Add a food token to the bird
        self.__dict__[hab][idx].cachedfood += 1
    
    #===========================================================================
    def editeggs(self, card, n):
        if type(card) is not BirdCard:
            raise TypeError('Card must be of type BirdCard.')
        elif n > 0 and card.laideggs == card.egg_capacity:
            raise Exception(f'{card} cannot hold any more eggs.')
        elif n < 0 and card.laideggs < n:
            raise Exception(f'{card} does not have enough eggs.')
        
        # Find the card
        hab, idx = self.findcard(card)

        # Lay that egg on that bird
        self.__dict__[hab][idx].laideggs += n
        self.eggs += n