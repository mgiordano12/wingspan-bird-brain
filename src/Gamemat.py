from BirdCard import BirdCard

class Gamemat:
    #===========================================================================
    def __init__(self):
        self.forest = list()
        self.grassland = list()
        self.wetland = list()

    #===========================================================================
    def playcard(self, card, habitat):
        if type(habitat) is not str or habitat not in ['forest', 'grassland', 'wetland']:
            raise Exception('Habitat must be a string in ["forest", "grassland", "wetland"].')
        elif type(card) is not BirdCard:
            raise TypeError('Card must of type BirdCard.')
        elif len(self.__dict__[habitat]) == 5:
            raise Exception(f'{habitat} already has 5 cards in it.')
        elif card.__dict__[habitat] is not True:
            raise Exception(f'{card} can not be played in {habitat}. It is not a valid habitat for this bird.')

        if habitat == 'forest':
            self.forest.append(card)
        elif habitat == 'grassland':
            self.grassland.append(card)
        elif habitat == 'wetland':
            self.wetland.append(card)

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
        self.__dict__[hab][idx].tuckedcards += 1
    
    #===========================================================================
    def cachefood(self, card):
        if type(card) is not BirdCard:
            raise TypeError('Card must be of type BirdCard.')
        
        # Find the card
        hab, idx = self.findcard(card)

        # Add a tucked card to the bird
        self.__dict__[hab][idx].cachedfood += 1
    
    #===========================================================================
    def layegg(self, card):
        if type(card) is not BirdCard:
            raise TypeError('Card must be of type BirdCard.')
        elif card.laideggs == card.egg_capacity:
            raise Exception(f'{card} cannot hold any more eggs.')
        
        # Find the card
        hab, idx = self.findcard(card)

        # Add a tucked card to the bird
        self.__dict__[hab][idx].laideggs += 1