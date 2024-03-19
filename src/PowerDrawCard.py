from BirdCardDeck import BirdCardDeck
from Player import Player

class PowerDrawCard:
    def __init__(self, numcards):
        self.numcards = numcards

    def performpower(self, player, birdcarddeck):
        assert type(player) is Player
        assert type(birdcarddeck) is BirdCardDeck
        cards = BirdCardDeck.draw_facedown_cards(n=self.numcards)
        player.editBirdCards(cards, remove=False)