from Player import Player
from initialize_resources import initialize_resources
from Gameplay_Constants import *
import numpy as np

class Game:
    #===========================================================================
    def __init__(self, num_players=1, player_names=['Joe'], seed=None):
        #### TODO: Initializing one player now, but will need to extend to multiple players in the future
        assert num_players == len(player_names)
        self.deck, self.bonus_card_deck, self.birdfeeder, self.end_of_round_goals = initialize_resources(seed=seed)
        self.players = dict()

        for i in range(num_players):
            initial_cards = self.deck.draw_facedown_cards(n=5)
            initial_bonus_cards = self.bonus_card_deck.draw_cards(n=2)
            self.players[player_names[i]] = Player(initial_cards, initial_bonus_cards, player_names[i])

    def __repr__(self):
        # TODO: Need to generalize to multiple players
        return (f"{self.birdfeeder},\n"
        f"{self.deck},\n"
        f"{self.end_of_round_goals},\n"
        f"{self.players[0]}")
