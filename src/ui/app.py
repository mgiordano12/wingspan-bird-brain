import sys
sys.path.append('../')
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

def clearLayout(layout):
    """ Used to clear all children out of layouts before redrawing them
    """
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()
        elif child.layout():
            clearLayout(child)

food = {
    'Fish': './images/food_fish.png', 'Rodent': './images/food_rodent.png', 
    'Fruit': './images/food_fruit.png', 'Invertebrate': './images/food_invertebrate.png', 
    'Seed': './images/food_seed.png', 'Invertebrate+Seed': './images/food_invertebrate+seed.png',
}
eorgs = {
    'Bird in Forest': './images/eorg_bird_in_forest.png', 
    'Bird in Grassland': './images/eorg_bird_in_grassland.png', 
    'Bird in Wetland': './images/eorg_bird_in_wetland.png',
    'Bowl Nest Bird with Egg': './images/eorg_bowl_nest_bird_w_egg.png',
    'Cavity Nest Bird with Egg': './images/eorg_cavity_nest_bird_w_egg.png',
    'Egg in Bowl Nest': './images/eorg_egg_in_bowl_nest.png',
    'Egg in Cavity Nest': './images/eorg_egg_in_cavity_nest.png',
    'Egg in Forest': './images/eorg_egg_in_forest.png',
    'Egg in Grassland': './images/eorg_egg_in_grassland.png',
    'Egg in Ground Nest': './images/eorg_egg_in_ground_nest.png',
    'Egg in Platform Nest': './images/eorg_egg_in_platform_nest.png',
    'Egg in Wetland': './images/eorg_egg_in_wetland.png',
    'Ground Nest Bird with Egg': './images/eorg_ground_nest_bird_w_egg.png',
    'Platform Nest Bird with Egg': './images/eorg_platform_nest_bird_w_egg.png',
    'Sets of Eggs in 3 Habitats': './images/eorg_sets_of_eggs_in_3_habitats.png',
    'Total Bird': './images/eorg_total_bird.png',
}

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
        self.forest = QWidget(styleSheet='background-color: green;')
        self.grassland = QWidget(styleSheet='background-color: yellow;')
        self.wetland = QWidget(styleSheet='background-color: blue;')
        self.birdDeckWidget = QWidget(styleSheet='background-color: gray;')
        self.birdDeckLayout = QGridLayout(self.birdDeckWidget)
        self.birdfeederLayout = QGridLayout()
        self.foodHandLayout = QGridLayout()
        self.birdHand = QWidget(styleSheet='background-color: gray;')
        self.birdHandLayout = QHBoxLayout(self.birdHand)
        self.bonusHandLayout = QHBoxLayout()

        # Forest habitat layout
        forestLayout = QHBoxLayout(self.forest)
        forestLayout.addWidget(QLabel(pixmap=QPixmap('./images/habitat_forest.png')))
        forestLayout.addWidget(QLabel(styleSheet='border: 1px solid black;'))
        forestLayout.addWidget(QLabel(styleSheet='border: 1px solid black;'))
        forestLayout.addWidget(QLabel(styleSheet='border: 1px solid black;'))
        forestLayout.addWidget(QLabel(styleSheet='border: 1px solid black;'))
        forestLayout.addWidget(QLabel(styleSheet='border: 1px solid black;'))

        # Grassland habitat
        grasslandLayout = QHBoxLayout(self.grassland)
        grasslandLayout.addWidget(QLabel(pixmap=QPixmap('./images/habitat_grassland.png')))
        grasslandLayout.addWidget(QLabel(styleSheet='border: 1px solid black;'))
        grasslandLayout.addWidget(QLabel(styleSheet='border: 1px solid black;'))
        grasslandLayout.addWidget(QLabel(styleSheet='border: 1px solid black;'))
        grasslandLayout.addWidget(QLabel(styleSheet='border: 1px solid black;'))
        grasslandLayout.addWidget(QLabel(styleSheet='border: 1px solid black;'))

        # Wetland habitat
        wetlandLayout = QHBoxLayout(self.wetland)
        wetlandLayout.addWidget(QLabel(pixmap=QPixmap('./images/habitat_wetland.png')))
        wetlandLayout.addWidget(QLabel(styleSheet='border: 1px solid black;'))
        wetlandLayout.addWidget(QLabel(styleSheet='border: 1px solid black;'))
        wetlandLayout.addWidget(QLabel(styleSheet='border: 1px solid black;'))
        wetlandLayout.addWidget(QLabel(styleSheet='border: 1px solid black;'))
        wetlandLayout.addWidget(QLabel(styleSheet='border: 1px solid black;'))

        # EORG Layout
        pixmap0 = QPixmap(eorgs[self.eorgMat.goals[0].name])
        pixmap1 = QPixmap(eorgs[self.eorgMat.goals[1].name])
        pixmap2 = QPixmap(eorgs[self.eorgMat.goals[2].name])
        pixmap3 = QPixmap(eorgs[self.eorgMat.goals[3].name])
        pixmap0 = pixmap0.scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        pixmap1 = pixmap1.scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        pixmap2 = pixmap2.scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        pixmap3 = pixmap3.scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        infoLayout = QGridLayout(self.info)
        infoLayout.addWidget(QLabel('Round: 1', styleSheet='font-weight: bold;'), 0, 0)
        infoLayout.addWidget(QLabel('Turns remaining: 8', styleSheet='font-weight: bold;'), 0, 2)
        infoLayout.addWidget(QLabel(pixmap=pixmap0), 2, 0)
        infoLayout.addWidget(QLabel(pixmap=pixmap1), 2, 1)
        infoLayout.addWidget(QLabel(pixmap=pixmap2), 2, 2)
        infoLayout.addWidget(QLabel(pixmap=pixmap3), 2, 3)

        
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

    #===========================================================================
    # Birdfeeder
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
            self.inFeederLayout.addWidget(QLabel(pixmap=QPixmap(food[die]).scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)))

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

    #===========================================================================
    # Food hand
    def renderFoodHand(self):
        clearLayout(self.foodHandLayout)
        self.foodHandLayout.addWidget(QLabel('Food in hand', styleSheet='font-weight: bold;'), 0, 0)
        self.foodHandLayout.addWidget(QLabel(pixmap=QPixmap('./images/food_invertebrate.png').scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)), 0, 2)
        self.foodHandLayout.addWidget(QLabel(f'x {self.player.food["Invertebrate"]}'), 0, 3)
        self.foodHandLayout.addWidget(QLabel(pixmap=QPixmap('./images/food_seed.png').scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)), 0, 4)
        self.foodHandLayout.addWidget(QLabel(f'x {self.player.food["Seed"]}'), 0, 5)
        self.foodHandLayout.addWidget(QLabel(pixmap=QPixmap('./images/food_fish.png').scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)), 1, 0)
        self.foodHandLayout.addWidget(QLabel(f'x {self.player.food["Fish"]}'), 1, 1)
        self.foodHandLayout.addWidget(QLabel(pixmap=QPixmap('./images/food_rodent.png').scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)), 1, 2)
        self.foodHandLayout.addWidget(QLabel(f'x {self.player.food["Rodent"]}'), 1, 3)
        self.foodHandLayout.addWidget(QLabel(pixmap=QPixmap('./images/food_fruit.png').scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)), 1, 4)
        self.foodHandLayout.addWidget(QLabel(f'x {self.player.food["Fruit"]}'), 1, 5)

    #===========================================================================
    # Bird card deck
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

    #===========================================================================
    # Bird cards in hand
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
    # Bonus cards in hand
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

#===============================================================================
# Main loop ====================================================================
#===============================================================================
app = QApplication(sys.argv)
window = WingspanAppWindow() 
window.show()
app.exec() # start event loop
