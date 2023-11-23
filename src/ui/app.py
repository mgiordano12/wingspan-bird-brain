import sys
sys.path.append('../')
from Birdfeeder import Birdfeeder
from EndOfRoundGoalMat import EndOfRoundGoalMat
from Player import Player

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QGridLayout, QLabel, QWidget, QHBoxLayout, QPushButton,
    QMessageBox
)
from PyQt6.QtGui import QPixmap

    

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

# Main window class ============================================================
class WingspanAppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('ca-caw! bird brain ca-caw!')

        # Initialize all of the game element objects
        self.birdfeeder = Birdfeeder()
        self.player = Player([], [])
        self.eorgMat = EndOfRoundGoalMat()

        # Initialize layouts
        self.centralLayout = QGridLayout()
        self.info = QWidget(styleSheet='background-color: gray;')
        self.forest = QWidget(styleSheet='background-color: green;')
        self.grassland = QWidget(styleSheet='background-color: yellow;')
        self.wetland = QWidget(styleSheet='background-color: blue;')
        self.birdCardDeck = QWidget(styleSheet='background-color: gray;')
        self.birdfeederLayout = QGridLayout()
        self.handFoodLayout = QGridLayout()
        self.handBirdCards = QWidget(styleSheet='background-color: gray;')
        self.handBonusCardsLayout = QHBoxLayout()

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

        # Birdfeeder Layout
        self.drawBirdfeeder()

        # Bird card deck layout
        birdCardDeckLayout = QGridLayout(self.birdCardDeck)
        birdCardDeckLayout.addWidget(QLabel('Bird cards', styleSheet='font-weight: bold;'), 0, 0)
        birdCardDeckLayout.addWidget(QLabel(styleSheet='border: 1px solid black;'), 1, 0)
        birdCardDeckLayout.addWidget(QLabel(styleSheet='border: 1px solid black;'), 1, 1)
        birdCardDeckLayout.addWidget(QLabel(styleSheet='border: 1px solid black;'), 1, 2)

        # Food in hand layout
        self.drawFoodHand()

        # Bird cards in hand layout
        handBirdCardsLayout = QHBoxLayout(self.handBirdCards)
        handBirdCardsLayout.addWidget(QPushButton(text='<', styleSheet='font-weight: bold;'))
        handBirdCardsLayout.addWidget(QLabel('1', styleSheet='border: 1px solid black;'))
        handBirdCardsLayout.addWidget(QLabel('2', styleSheet='border: 1px solid black;'))
        handBirdCardsLayout.addWidget(QLabel('3', styleSheet='border: 1px solid black;'))
        handBirdCardsLayout.addWidget(QLabel('4', styleSheet='border: 1px solid black;'))
        handBirdCardsLayout.addWidget(QLabel('5', styleSheet='border: 1px solid black;'))
        handBirdCardsLayout.addWidget(QPushButton(text='>', styleSheet='font-weight: bold;'))

        # Bonus cards in hand layout
        self.handBonusCardsLayout.addWidget(QPushButton(text='<', styleSheet='font-weight: bold;'))
        self.handBonusCardsLayout.addWidget(QLabel('1', styleSheet='border: 1px solid black;'))
        self.handBonusCardsLayout.addWidget(QLabel('2', styleSheet='border: 1px solid black;'))
        self.handBonusCardsLayout.addWidget(QPushButton(text='>', styleSheet='font-weight: bold;'))
        
        # Add layouts to central layout
        self.centralLayout.addWidget(self.forest, 0, 0)
        self.centralLayout.addWidget(self.info, 0, 1)
        self.centralLayout.addWidget(self.grassland, 1, 0)
        self.centralLayout.addLayout(self.birdfeederLayout, 1, 1)
        self.centralLayout.addWidget(self.wetland, 2, 0)
        self.centralLayout.addWidget(self.birdCardDeck, 2, 1)
        self.centralLayout.addLayout(self.handBonusCardsLayout, 3, 0)
        self.centralLayout.addLayout(self.handFoodLayout, 3, 1)
        self.centralLayout.addWidget(self.handBirdCards, 4, 0, 1, 2)

        # Set central layout as central widget for layout
        w = QWidget()
        w.setLayout(self.centralLayout)
        self.setCentralWidget(w)

    #===============================================================================
    def drawBirdfeeder(self):
        clearLayout(self.birdfeederLayout)
        self.inFeederLayout = QHBoxLayout()
        self.takeFoodButton = QPushButton('Take')
        self.takeFoodButton.clicked.connect(self.takeFood)
        self.rollButton = QPushButton('Roll')
        self.rollButton.clicked.connect(self.rollFeeder)
        self.birdfeederLayout.addWidget(QLabel('In feeder:', styleSheet='font-weight: bold;'), 0, 0)
        self.birdfeederLayout.addWidget(self.takeFoodButton, 0, 1)
        self.birdfeederLayout.addWidget(self.rollButton, 0, 2)
        self.birdfeederLayout.addLayout(self.inFeederLayout, 1, 0, 1, 3)
        for die in self.birdfeeder.food:
            self.inFeederLayout.addWidget(QLabel(pixmap=QPixmap(food[die])))

    #===============================================================================
    def rollFeeder(self):
        try:
            self.birdfeeder.reroll()
        except Exception as e:
            QMessageBox(text=repr(e)).exec()
        self.drawBirdfeeder()

    #===============================================================================
    def takeFood(self):
        from PyQt6.QtWidgets import QInputDialog
        food, ok = QInputDialog().getItem(self, 'Choose food from birdfeeder', 'Choices', self.birdfeeder.food, 0, False)
        if ok and food=='Invertebrate+Seed':
            # Another popup to choose which one to take
            food_to_remove = 'Invertebrate+Seed'
            food, ok = QInputDialog().getItem(self, 'Choose food from birdfeeder', 'Choices', ['Invertebrate', 'Seed'])
        elif ok:
            food_to_remove = food
        if ok:
            # Take food from the feeder and put it into the player's hand
            self.birdfeeder.take(food_to_remove)
            self.player.food[food] += 1
            # Redraw the board
            self.drawBirdfeeder()
            self.drawFoodHand()

    #==========================================================================
    def drawFoodHand(self):
        clearLayout(self.handFoodLayout)
        self.handFoodLayout.addWidget(QLabel('Food in hand', styleSheet='font-weight: bold;'), 0, 0)
        self.handFoodLayout.addWidget(QLabel(pixmap=QPixmap('./images/food_invertebrate.png')), 0, 1)
        self.handFoodLayout.addWidget(QLabel(f'x {self.player.food["Invertebrate"]}'), 0, 2)
        self.handFoodLayout.addWidget(QLabel(pixmap=QPixmap('./images/food_seed.png')), 0, 3)
        self.handFoodLayout.addWidget(QLabel(f'x {self.player.food["Seed"]}'), 0, 4)
        self.handFoodLayout.addWidget(QLabel(pixmap=QPixmap('./images/food_fish.png')), 1, 0)
        self.handFoodLayout.addWidget(QLabel(f'x {self.player.food["Fish"]}'), 1, 1)
        self.handFoodLayout.addWidget(QLabel(pixmap=QPixmap('./images/food_rodent.png')), 1, 2)
        self.handFoodLayout.addWidget(QLabel(f'x {self.player.food["Rodent"]}'), 1, 3)
        self.handFoodLayout.addWidget(QLabel(pixmap=QPixmap('./images/food_fruit.png')), 1, 4)
        self.handFoodLayout.addWidget(QLabel(f'x {self.player.food["Fruit"]}'), 1, 5)

# Main loop ====================================================================
app = QApplication(sys.argv)
window = WingspanAppWindow() 
window.show()
app.exec() # start event loop
