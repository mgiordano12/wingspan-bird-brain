from Player import Player
from initialize_resources import initialize_resources

#### TODO: Initializing one player now, but will need to extend to multiple players in the future
# I'm going to make this a list of one player in the hopes that makes switching to multiple easier in the future
NUM_PLAYERS = 1
PLAYER_NAMES = ['Joe']

deck, bonus_card_deck, birdfeeder, end_of_round_goals = initialize_resources(seed=6)

players = []
for i in range(NUM_PLAYERS):
    initial_cards = deck.draw_facedown_cards(n=5)
    initial_bonus_cards = bonus_card_deck.draw_cards(n=2)
    players.append(Player(initial_cards, initial_bonus_cards, PLAYER_NAMES[i]))

print(f"Birdfeeder: {birdfeeder}")
print(f"Deck {deck}")
print(f"End Goals {end_of_round_goals}")
print(players[0])