import sys
sys.path.append('./src/')
sys.path.append('./src/ui/')
from BirdCardDeck import BirdCardDeck
from BirdCardWidget import BirdCardWidget
from Birdfeeder import Birdfeeder
from BonusCardDeck import BonusCardDeck
from BonusCardWidget import BonusCardWidget
from EndOfRoundGoalMat import EndOfRoundGoalMat
from Player import Player
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QGridLayout, QLabel, QWidget, QHBoxLayout, QPushButton,
    QMessageBox, QInputDialog, QScrollArea
)
from PyQt6.QtGui import QPixmap
from StartingMaterialsPopup import StartingMaterialsPopup
from imagepaths import eorg_paths, habitat_paths, food_paths
from SpendFoodPopup import SpendFoodPopup
from clearlayout import clearLayout

#===============================================================================
# Main window class ============================================================
#===============================================================================
class WingspanAppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('ca-caw! bird brain ca-caw!')

        # Initialize all of the game element objects
        self.birdfeeder = Birdfeeder()
        self.eorgMat = EndOfRoundGoalMat()
        self.birdCardDeck = BirdCardDeck()
        self.bonusCardDeck = BonusCardDeck()
        self.birdHandStartIdx = 0 # starting index for displayed bird card hand
        self.bonusHandStartIdx = 0 # index for bonus cards

        # Popup to choose bird cards, bonus cards, and food. Then init player
        startingPopup = StartingMaterialsPopup(
            birdcards=self.birdCardDeck.draw_facedown_cards(n=5),
            bonuscards=self.bonusCardDeck.draw_cards(n=2),
        )
        if startingPopup.exec():
            birdcards, bonuscards, food = startingPopup.getInputs()
        else:
            raise Exception('Starting resource assignment canceled.')
        self.player = Player(birdcards, bonuscards)
        food = {
            'Invertebrate': 0 if 'Invertebrate' in food else -1,
            'Seed': 0 if 'Seed' in food else -1,
            'Fruit': 0 if 'Fruit' in food else -1,
            'Fish': 0 if 'Fish' in food else -1,
            'Rodent': 0 if 'Rodent' in food else -1,
        }
        self.player.editFood(food)

        # Initialize layouts
        self.centralLayout = QGridLayout()
        self.info = QWidget(styleSheet='background-color: gray;')
        self.infoLayout = QGridLayout(self.info)
        self.forest = QWidget(styleSheet='background-color: forestgreen;')
        self.forestLayout = QGridLayout(self.forest)
        self.grassland = QWidget(styleSheet='background-color: goldenrod;')
        self.grasslandLayout = QGridLayout(self.grassland)
        self.wetland = QWidget(styleSheet='background-color: cornflowerblue;')
        self.wetlandLayout = QGridLayout(self.wetland)
        self.birdDeckWidget = QWidget(styleSheet='background-color: gray;')
        self.birdDeckLayout = QGridLayout(self.birdDeckWidget)
        self.birdfeederLayout = QGridLayout()
        self.foodHandLayout = QGridLayout()
        self.birdHand = QWidget(styleSheet='background-color: gray;')
        self.birdHandLayout = QHBoxLayout(self.birdHand)
        self.bonusHandLayout = QHBoxLayout()

        self.render()

    #===========================================================================
    # Rendering functions
    def render(self):
        clearLayout(self.infoLayout)
        # EORG Layout
        pixmap0 = QPixmap(eorg_paths[self.eorgMat.goals[0].name])
        pixmap1 = QPixmap(eorg_paths[self.eorgMat.goals[1].name])
        pixmap2 = QPixmap(eorg_paths[self.eorgMat.goals[2].name])
        pixmap3 = QPixmap(eorg_paths[self.eorgMat.goals[3].name])
        pixmap0 = pixmap0.scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        pixmap1 = pixmap1.scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        pixmap2 = pixmap2.scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        pixmap3 = pixmap3.scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.infoLayout.addWidget(QLabel('Round: 1', styleSheet='font-weight: bold;'), 0, 0)
        self.infoLayout.addWidget(QLabel('Turns remaining: 8', styleSheet='font-weight: bold;'), 0, 2)
        self.infoLayout.addWidget(QLabel(pixmap=pixmap0), 2, 0)
        self.infoLayout.addWidget(QLabel(pixmap=pixmap1), 2, 1)
        self.infoLayout.addWidget(QLabel(pixmap=pixmap2), 2, 2)
        self.infoLayout.addWidget(QLabel(pixmap=pixmap3), 2, 3)

        # Render fns for all of the other elements
        self.renderForest() # forest habitat layout
        self.renderGrassland() # grassland habitat
        self.renderWetland() # wetland habitat    
        self.renderBirdfeeder() # Birdfeeder Layout
        self.renderBirdCardDeck() # Bird card deck layout
        self.renderFoodHand() # Food in hand layout
        self.renderBirdHand() # Bird cards in hand layout
        self.renderBonusHand() # Bonus cards in hand layout
        
        # Add layouts to central layout
        self.centralLayout.addWidget(self.forest, 0, 0)
        self.centralLayout.addWidget(self.info, 0, 1)
        self.centralLayout.addWidget(self.grassland, 1, 0)
        self.centralLayout.addLayout(self.birdfeederLayout, 1, 1)
        self.centralLayout.addWidget(self.wetland, 2, 0)
        self.centralLayout.addWidget(self.birdDeckWidget, 2, 1)
        self.centralLayout.addLayout(self.bonusHandLayout, 3, 0)
        self.centralLayout.addLayout(self.foodHandLayout, 3, 1)
        self.centralLayout.addWidget(self.birdHand, 4, 0, 1, 2)

        # Create a widget to hold the central layout
        w = QWidget()
        w.setLayout(self.centralLayout)

        # Make the central widget scrollable
        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll.setWidgetResizable(True)
        scroll.setWidget(w)

        # Set the scrollable widget as the central widget of the window
        self.setCentralWidget(scroll)

    def renderForest(self):
        clearLayout(self.forestLayout)
        forest = self.player.gamemat.habitats['forest']
        self.forestLayout.addWidget(QLabel(pixmap=QPixmap(habitat_paths['Forest'])), 0, 0)
        self.forestBtn = QPushButton('Play card', styleSheet='background-color: white;')
        self.forestBtn.clicked.connect(lambda: self.playCard('forest'))
        self.forestLayout.addWidget(self.forestBtn, 1, 0)
        for i in range(5):
            card = BirdCardWidget(forest[i]) if i < len(forest) else QLabel(styleSheet='border: 1px solid black;')
            self.forestLayout.addWidget(card, 0, i+1, 2, 1)

    def renderGrassland(self):
        clearLayout(self.grasslandLayout)
        self.grasslandLayout.addWidget(QLabel(pixmap=QPixmap(habitat_paths['Grassland'])), 0, 0)
        self.grasslandPlayCardBtn = QPushButton('Play card', styleSheet='background-color: white;')
        self.grasslandPlayCardBtn.clicked.connect(lambda: self.playCard('grassland'))
        self.grasslandLayout.addWidget(self.grasslandPlayCardBtn, 1, 0)
        self.grasslandLayEggsBtn = QPushButton('Lay eggs', styleSheet='background-color: white;')
        self.grasslandLayEggsBtn.clicked.connect(self.layeggoncard)
        self.grasslandLayout.addWidget(self.grasslandLayEggsBtn, 2, 0)
        grassland = self.player.gamemat.habitats['grassland']
        for i in range(5):
            card = BirdCardWidget(grassland[i]) if i < len(grassland) else QLabel(styleSheet='border: 1px solid black;')
            self.grasslandLayout.addWidget(card, 0, i+1, 3, 1)

    def renderWetland(self):
        clearLayout(self.wetlandLayout)
        wetland = self.player.gamemat.habitats['wetland']
        self.wetlandLayout.addWidget(QLabel(pixmap=QPixmap(habitat_paths['Wetland'])), 0, 0)
        self.wetlandBtn = QPushButton('Play card', styleSheet='background-color: white;')
        self.wetlandBtn.clicked.connect(lambda: self.playCard('wetland'))
        self.wetlandLayout.addWidget(self.wetlandBtn, 1, 0)
        for i in range(5):
            card = BirdCardWidget(wetland[i]) if i < len(wetland) else QLabel(styleSheet='border: 1px solid black;')
            self.wetlandLayout.addWidget(card, 0, i+1, 2, 1)

    def renderBirdfeeder(self):
        clearLayout(self.birdfeederLayout)
        self.inFeederLayout = QHBoxLayout()
        self.takeFoodButton = QPushButton('Take')
        self.takeFoodButton.clicked.connect(self.takeFood)
        self.rollButton = QPushButton('Roll')
        self.rollButton.clicked.connect(self.rollFeeder)
        self.birdfeederLayout.addWidget(QLabel('Birdfeeder:', styleSheet='font-weight: bold;'), 0, 0)
        self.birdfeederLayout.addWidget(self.takeFoodButton, 0, 1)
        self.birdfeederLayout.addWidget(self.rollButton, 0, 2)
        self.birdfeederLayout.addLayout(self.inFeederLayout, 1, 0, 1, 3)
        for die in self.birdfeeder.food:
            self.inFeederLayout.addWidget(QLabel(pixmap=QPixmap(food_paths[die])))

    def renderFoodHand(self):
        clearLayout(self.foodHandLayout)
        self.foodHandLayout.addWidget(QLabel('Food in hand', styleSheet='font-weight: bold;'), 0, 0)
        self.foodHandLayout.addWidget(QLabel(pixmap=QPixmap(food_paths['Invertebrate']).scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)), 0, 2)
        self.foodHandLayout.addWidget(QLabel(f'x {self.player.food['Invertebrate']}'), 0, 3)
        self.foodHandLayout.addWidget(QLabel(pixmap=QPixmap(food_paths['Seed']).scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)), 0, 4)
        self.foodHandLayout.addWidget(QLabel(f'x {self.player.food['Seed']}'), 0, 5)
        self.foodHandLayout.addWidget(QLabel(pixmap=QPixmap(food_paths['Fish']).scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)), 1, 0)
        self.foodHandLayout.addWidget(QLabel(f'x {self.player.food['Fish']}'), 1, 1)
        self.foodHandLayout.addWidget(QLabel(pixmap=QPixmap(food_paths['Rodent']).scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)), 1, 2)
        self.foodHandLayout.addWidget(QLabel(f'x {self.player.food['Rodent']}'), 1, 3)
        self.foodHandLayout.addWidget(QLabel(pixmap=QPixmap(food_paths['Fruit']).scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)), 1, 4)
        self.foodHandLayout.addWidget(QLabel(f'x {self.player.food['Fruit']}'), 1, 5)

    def renderBirdCardDeck(self):
        clearLayout(self.birdDeckLayout)
        self.birdDeckLayout.addWidget(QLabel('Bird card deck', styleSheet='font-weight: bold;'), 0, 0)
        self.drawFacedownBirdCardBtn = QPushButton('Draw facedown card')
        self.drawFacedownBirdCardBtn.clicked.connect(self.drawFacedownBirdCard)
        self.birdDeckLayout.addWidget(self.drawFacedownBirdCardBtn, 0, 1)
        self.drawFaceupBirdCardBtn = QPushButton('Draw faceup card')
        self.drawFaceupBirdCardBtn.clicked.connect(self.drawFaceupBirdCard)
        self.birdDeckLayout.addWidget(self.drawFaceupBirdCardBtn, 0, 2)
        for i in range(3):
            card = self.birdCardDeck.faceup_cards[i]
            if isinstance(card, type(None)):
                cw = QLabel(styleSheet='border: 1px solid black;')
            else:
                cw = BirdCardWidget(card)
            self.birdDeckLayout.addWidget(cw, 1, i)

    def renderBonusHand(self):
        clearLayout(self.bonusHandLayout)
        self.bonusHandLeftBtn = QPushButton(text='<', styleSheet='font-weight: bold;')
        self.bonusHandLeftBtn.clicked.connect(self.bonusHandLeft)
        self.bonusHandLayout.addWidget(self.bonusHandLeftBtn)
        end = self.bonusHandStartIdx+2 if self.bonusHandStartIdx+2 < len(self.player.bonuscards) else len(self.player.bonuscards)
        for i in range(self.bonusHandStartIdx, end):
            self.bonusHandLayout.addWidget(BonusCardWidget(self.player.bonuscards[i]))
        self.bonusHandRightBtn = QPushButton(text='>', styleSheet='font-weight: bold;')
        self.bonusHandRightBtn.clicked.connect(self.bonusHandRight)
        self.bonusHandLayout.addWidget(self.bonusHandRightBtn)
    def bonusHandLeft(self):
        if self.bonusHandStartIdx > 0:
            self.bonusHandStartIdx -= 1
            self.renderBonusHand()
    def bonusHandRight(self):
        if self.bonusHandStartIdx < len(self.player.bonuscards) - 2:
            self.bonusHandStartIdx += 1
            self.renderBonusHand()

    def renderBirdHand(self):
        clearLayout(self.birdHandLayout)
        self.birdHandLeftBtn = QPushButton(text='<', styleSheet='font-weight: bold;')
        self.birdHandLeftBtn.clicked.connect(self.birdHandLeft)
        self.birdHandLayout.addWidget(self.birdHandLeftBtn)
        end = self.birdHandStartIdx+5 if self.birdHandStartIdx+5 < len(self.player.birdcards) else len(self.player.birdcards)
        for i in range(self.birdHandStartIdx, end):
            self.birdHandLayout.addWidget(BirdCardWidget(self.player.birdcards[i]))
        self.birdHandRightBtn = QPushButton(text='>', styleSheet='font-weight: bold;')
        self.birdHandRightBtn.clicked.connect(self.birdHandRight)
        self.birdHandLayout.addWidget(self.birdHandRightBtn)
    def birdHandLeft(self):
        if self.birdHandStartIdx > 0:
            self.birdHandStartIdx -= 1
            self.renderBirdHand()
    def birdHandRight(self):
        if self.birdHandStartIdx < len(self.player.birdcards) - 5:
            self.birdHandStartIdx += 1
            self.renderBirdHand()

    #===========================================================================
    # Game action fns
    def rollFeeder(self):
        try:
            self.birdfeeder.reroll()
        except Exception as e:
            QMessageBox(text=repr(e)).exec()
        self.renderBirdfeeder()

    def takeFood(self):
        food, ok = QInputDialog().getItem(self, 'Choose food from birdfeeder', 'Choices', self.birdfeeder.food, 0, False)
        if ok and food=='Invertebrate+Seed':
            # Another popup to choose which one to take
            food_to_remove = 'Invertebrate+Seed'
            food, ok = QInputDialog().getItem(self, 'Choose invertebrate or seed', 'Choices', ['Invertebrate', 'Seed'])
        elif ok:
            food_to_remove = food
        if ok:
            # Take food from the feeder and put it into the player's hand
            self.birdfeeder.take(food_to_remove)
            self.player.food[food] += 1
            # Redraw the board
            self.renderBirdfeeder()
            self.renderFoodHand()

    def drawFacedownBirdCard(self):
        card = self.birdCardDeck.draw_facedown_cards(n=1)
        self.player.editBirdCards(card)
        self.renderBirdHand()
        self.renderBirdCardDeck()

    def drawFaceupBirdCard(self):
        idx, ok = QInputDialog().getItem(self, 'Choose index of card to take', 'Index (indices go L --> R)', ['0', '1', '2'], 0, False)
        if ok:
            card = self.birdCardDeck.draw_faceup_card(i=int(idx))
            self.player.editBirdCards(card)
            self.birdCardDeck.refill_faceup_cards() # @TODO: move this to the end of turn update sequence for actual gameplay 
            self.renderBirdHand()
            self.renderBirdCardDeck()

    def layeggoncard(self):
        cardstr, ok = QInputDialog().getItem(self, 
                                             'Choose bird to lay egg on', 
                                             'Choices', 
                                             [str(c) for h in self.player.gamemat.habitats.values() for c in h], 
                                             0, False)
        if ok:
            card = [c for c in self.player.getplayedcards() if c.__repr__() == cardstr]
            assert len(card) == 1
            card = card[0]
            self.player.layegg(card)
            # Render habitats to show new egg
            self.renderForest()
            self.renderGrassland()
            self.renderWetland()

    def choosecardtospendegg(self):
        cardstr, ok = QInputDialog().getItem(self, 
                                             'Choose bird to take egg from', 
                                             'Choices', 
                                             [str(c) for c in self.player.getplayedcards() if c.laideggs > 0], 
                                             0, False)
        if ok:
            card = [c for c in self.player.getplayedcards() if c.__repr__() == cardstr]
            assert len(card) == 1
            card = card[0]
        else:
            card = None
        return card
    
    def choosefoodtospend(self, card):
        """ card is the card being played
        """
        spendFoodPopup = SpendFoodPopup(card)
        if spendFoodPopup.exec():
            foodtospend = spendFoodPopup.get_inputs()
        else:
            raise Exception('Food spending canceled.')
        return foodtospend

    def playCard(self, habitat):
        cardstr, ok = QInputDialog().getItem(self, 
                                             f'Choose bird to play in {habitat}', 
                                             'Choices', 
                                             [str(c) for c in self.player.birdcards], 
                                             0, False)
        if ok:
            card = [c for c in self.player.birdcards if c.__repr__() == cardstr]
            assert len(card) == 1
            card = card[0]

            # Determine egg cost and if player can pay it
            eggcost = self.player.gamemat.determineeggcost(habitat)
            player_laideggs = sum([c.laideggs for c in self.player.getplayedcards()])
            if player_laideggs < eggcost:
                raise Exception(f'Player cannot pay egg cost. Player only has {player_laideggs} of {eggcost} required eggs.')

            # Choose eggs to spend
            spenteggs = 0
            while spenteggs < eggcost:
                try:
                    eggcard = self.choosecardtospendegg()
                    if eggcard is not None:
                        eggcard.removeegg()
                        self.renderForest()
                        self.renderGrassland()
                        self.renderWetland()
                        spenteggs += 1
                except Exception as e:
                    QMessageBox(text=repr(e)).exec()

            # Choose food to spend
            if card.total_food_cost > 0:
                foodtospend = self.choosefoodtospend(card)
            
            try:
                self.player.playcard(card, habitat)
                self.renderForest()
                self.renderGrassland()
                self.renderWetland()
                self.renderBirdHand()
            except Exception as e:
                QMessageBox(text=repr(e)).exec()

#===============================================================================
# Main loop ====================================================================
#===============================================================================
app = QApplication(sys.argv)
window = WingspanAppWindow() 
window.show()
app.exec() # start event loop
