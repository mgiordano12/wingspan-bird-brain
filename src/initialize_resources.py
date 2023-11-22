from BirdCardDeck import BirdCardDeck
from Birdfeeder import Birdfeeder
from BonusCardDeck import BonusCardDeck
from EndOfRoundGoalMat import EndOfRoundGoalMat
def initialize_resources(decks=['originalcore'],seed=0):
    deck = BirdCardDeck(seed=seed)
    bonus_card_deck = BonusCardDeck(seed=seed)
    # TODO: Seeding birdfeeder not yet implemented
    birdfeeder = Birdfeeder()
    end_round_goals = EndOfRoundGoalMat()
    return deck, bonus_card_deck, birdfeeder, end_round_goals