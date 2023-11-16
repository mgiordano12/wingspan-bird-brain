from Hand import Hand
from Gamemat import Gamemat
from BirdCard import BirdCard
import names

class Player:
    #===================================================================================================================
    def __init__(self, name = None):
        if name is None:
            # Low likelihood this could assign players the same name at random...
            self.name = names.get_first_name()
        else:
            self.name = name
        self.current_hand = Hand()
        self.current_gamemat = Gamemat()
        self.assign_starting_materials()

    #===================================================================================================================
    def assign_starting_materials(self):
        """
        At start, players get:
            1) 1 of each food token (total of 5)
            2) 5 bird cards at random
            3) 2 bonus cards
        """

        self.food_tokens = {'Rat' : 0, 'Slug' : 0, 'Wheat' : 0, 'Cherry' : 0, 'Fish' : 0}
        self.eggs = 0
        self.bonus_cards = []
        self.action_cubes = 8  # Assuming a 2-3 player game for this example

    def start_game_setup(self, initial_bird_card : list):
        

    def __repr__(self):
        return (f"Player(Name: {self.name}, Hand: {self.hand}, GameMat: {self.game_mat}, "
                f"Food Tokens: {self.food_tokens}, Eggs: {self.eggs}, Bonus Cards: {self.bonus_cards}, "
                f"Action Cubes: {self.action_cubes})")
