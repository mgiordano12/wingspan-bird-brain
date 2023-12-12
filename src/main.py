import sys
sys.path.append('./src')
sys.path.append('./src/ui')
from BirdCardDeck import BirdCardDeck
from Birdfeeder import Birdfeeder
from BonusCardDeck import BonusCardDeck
from Player import Player
from EndOfRoundGoalMat import EndOfRoundGoalMat
from StartingMaterialsPopup import StartingMaterialsPopup
from PyQt6.QtWidgets import QApplication, QMainWindow
from WingspanAppWindow import WingspanAppWindow

#### TODO: Initializing one player now, but will need to extend to multiple players in the future
# I'm going to make this a list of one player in the hopes that makes switching to multiple easier in the future
NUM_PLAYERS = 1 
PLAYER_NAMES = ['Joe']

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.show()

    deck = BirdCardDeck()
    bonus_card_deck = BonusCardDeck()
    birdfeeder = Birdfeeder()
    eorgmat = EndOfRoundGoalMat()

    players = []
    for i in range(NUM_PLAYERS):
        startingPopup = StartingMaterialsPopup(birdcards=deck.draw_facedown_cards(n=5), 
                                            bonuscards=bonus_card_deck.draw_cards(n=2))
        startingPopup.show()
        if startingPopup.exec():
            birdcards, bonuscards, food = startingPopup.getInputs()
            food = {'Invertebrate': 1 if 'Invertebrate' in food else 0,
                    'Seed': 1 if 'Seed' in food else 0,
                    'Fruit': 1 if 'Fruit' in food else 0,
                    'Fish': 1 if 'Fish' in food else 0,
                    'Rodent': 1 if 'Rodent' in food else 0}
            newplayer = Player(birdcards, bonuscards, food)
            players.append(newplayer)
        else:
            raise Exception('Starting resource assignment canceled.')
    
    window.close()

    window = WingspanAppWindow(players[0], birdfeeder, eorgmat, deck, bonus_card_deck)
    window.show()

    app.exec()

    # players = []
    # for i in range(NUM_PLAYERS):
    #     initial_cards = deck.draw_facedown_cards(n=5)
    #     initial_bonus_cards = bonus_card_deck.draw_cards(n=2)
    #     startingPopup = StartingMaterialsPopup(birdcards=initial_cards, bonuscards=initial_bonus_cards)
    #     startingPopup.show()
    #     if startingPopup.exec():
    #         birdcards, bonuscards, food = startingPopup.getInputs()
    #     else:
    #         raise Exception('Starting resource assignment canceled.')
    #     players.append(Player(initial_cards, initial_bonus_cards, PLAYER_NAMES[i]))

    # print(players[0])