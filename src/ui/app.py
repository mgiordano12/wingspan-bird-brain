from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QGridLayout, QLabel, QWidget, QHBoxLayout, QPushButton
)
from PyQt6.QtGui import QPixmap
import sys

# Main window class ============================================================
class WingspanAppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('ca-caw! bird brain ca-caw!')

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
        infoLayout = QGridLayout(self.info)
        infoLayout.addWidget(QLabel('Round: 1', styleSheet='font-weight: bold;'), 0, 0)
        infoLayout.addWidget(QLabel('Turns remaining: 8', styleSheet='font-weight: bold;'), 0, 2)
        infoLayout.addWidget(QLabel('Rd. 1', styleSheet='border: 1px solid black;'), 2, 0)
        infoLayout.addWidget(QLabel('Rd. 2', styleSheet='border: 1px solid black;'), 2, 1)
        infoLayout.addWidget(QLabel('Rd. 3', styleSheet='border: 1px solid black;'), 2, 2)
        infoLayout.addWidget(QLabel('Rd. 4', styleSheet='border: 1px solid black;'), 2, 3)

        # Birdfeeder Layout
        self.birdfeederLayout.addWidget(QLabel('In feeder:', styleSheet='font-weight: bold;'), 0, 0)
        self.birdfeederLayout.addWidget(QLabel(styleSheet='border: 1px solid black;'), 1, 0)
        self.birdfeederLayout.addWidget(QLabel('Out of feeder:', styleSheet='font-weight: bold;'), 0, 1)
        self.birdfeederLayout.addWidget(QLabel(styleSheet='border: 1px solid black;'), 1, 1)

        # Bird card deck layout
        birdCardDeckLayout = QGridLayout(self.birdCardDeck)
        birdCardDeckLayout.addWidget(QLabel('Bird cards', styleSheet='font-weight: bold;'), 0, 0)
        birdCardDeckLayout.addWidget(QLabel(styleSheet='border: 1px solid black;'), 1, 0)
        birdCardDeckLayout.addWidget(QLabel(styleSheet='border: 1px solid black;'), 1, 1)
        birdCardDeckLayout.addWidget(QLabel(styleSheet='border: 1px solid black;'), 1, 2)

        # Food in hand layout
        self.handFoodLayout.addWidget(QLabel('Food in hand', styleSheet='font-weight: bold;'), 0, 0)
        self.handFoodLayout.addWidget(QLabel(pixmap=QPixmap('./images/food_invertebrate.png')), 0, 1)
        self.handFoodLayout.addWidget(QLabel('x 0'), 0, 2)
        self.handFoodLayout.addWidget(QLabel(pixmap=QPixmap('./images/food_seed.png')), 0, 3)
        self.handFoodLayout.addWidget(QLabel('x 0'), 0, 4)
        self.handFoodLayout.addWidget(QLabel(pixmap=QPixmap('./images/food_fish.png')), 1, 0)
        self.handFoodLayout.addWidget(QLabel('x 0'), 1, 1)
        self.handFoodLayout.addWidget(QLabel(pixmap=QPixmap('./images/food_rodent.png')), 1, 2)
        self.handFoodLayout.addWidget(QLabel('x 0'), 1, 3)
        self.handFoodLayout.addWidget(QLabel(pixmap=QPixmap('./images/food_fruit.png')), 1, 4)
        self.handFoodLayout.addWidget(QLabel('x 0'), 1, 5)

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

# Main loop ====================================================================
app = QApplication(sys.argv)
window = WingspanAppWindow() 
window.show()
app.exec() # start event loop
