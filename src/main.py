from BirdCardDeck import BirdCardDeck
from Birdfeeder import Birdfeeder
from BonusCardDeck import BonusCardDeck
from Player import Player

#### TODO: Initializing one player now, but will need to extend to multiple players in the future
# I'm going to make this a list of one player in the hopes that makes switching to multiple easier in the future
NUM_PLAYERS = 1 
PLAYER_NAMES = ['Joe']

deck = BirdCardDeck()
bonus_card_deck = BonusCardDeck()
birdfeeder = Birdfeeder()

players = []
for i in range(NUM_PLAYERS):
    initial_cards = deck.draw_facedown_cards(n=5)
    initial_bonus_cards = bonus_card_deck.draw_cards(n=2)
    players.append(Player(initial_cards, initial_bonus_cards, PLAYER_NAMES[i]))

print(players[0])