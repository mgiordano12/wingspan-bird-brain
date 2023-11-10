from Hand import Hand
from Gamemat import Gamemat
from BirdCard import BirdCard
import names

class Player:
    #===================================================================================================================
    def __init__(self, name = None):
        if name == None:
            # Low likelihood this could assign players the same name at random...
            self.name = names.get_first_name()
        else:
            self.name == name
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

        self.food_tokens = []
        self.eggs = 0
        self.bonus_cards = []
        self.action_cubes = 8  # Assuming a 2-3 player game for this example

    def start_game_setup(self, initial_bird_cards, initial_food_tokens):
        # Players choose bird cards to keep. For each card kept, they must discard one other starting resource.
        number_of_cards_to_keep = random.randint(1, 5)
        self.hand.add(initial_bird_cards)
        self.hand.choose_cards_to_keep(number_of_cards_to_keep)

        # Assign food tokens based on the number of bird cards kept.
        # The total of bird cards and food tokens must be 5.
        food_tokens_to_keep = 5 - number_of_cards_to_keep
        self.food_tokens = initial_food_tokens[:food_tokens_to_keep]

        # Deal two bonus cards and choose one to keep
        self.bonus_cards = random.sample(initial_bird_cards, 2)  # Assuming bonus cards are the same type as bird cards for this example
        self.bonus_cards = [self.bonus_cards[0]]  # Keep one bonus card

    def __repr__(self):
        return (f"Player(Name: {self.name}, Hand: {self.hand}, GameMat: {self.game_mat}, "
                f"Food Tokens: {self.food_tokens}, Eggs: {self.eggs}, Bonus Cards: {self.bonus_cards}, "
                f"Action Cubes: {self.action_cubes})")
