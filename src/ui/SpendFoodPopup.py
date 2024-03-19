import sys
from BirdCard import BirdCard
from PyQt6.QtWidgets import QGridLayout, QDialog, QLabel, QDialogButtonBox, QHBoxLayout, QPushButton
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from imagepaths import food_paths
from clearlayout import clearLayout

class SpendFoodPopup(QDialog):

    def __init__(self, card):
        """
        card is the card being played
        """
        if type(card) is not BirdCard:
            raise Exception('`card` in SpendFoodPopup.__init__() must be of type BirdCard')
        
        super().__init__()

        cardfoods = [('Invertebrate', card.invertebrate), ('Seed', card.seed), 
                     ('Fruit', card.fruit), ('Fish', card.fish), 
                     ('Rodent', card.rodent), ('Wild', card.wild_food)]
        self.foodtospend = {'Invertebrate': 0, 'Seed': 0, 'Fruit': 0, 
                            'Fish': 0, 'Rodent': 0}

        self.layout = QGridLayout(self)

        # Layout showing the food cost of the bird
        self.foodcostLayout = QHBoxLayout()
        self.layout.addLayout(self.foodcostLayout, 0, 0)
        self.foodcostLayout.addWidget(QLabel('Cost of card:', styleSheet='font-weight: bold;'))
        sep = '/' if card.slash_food_cost else '+'
        for foodtype, cnt in cardfoods:
            if cnt > 0:
                self.foodcostLayout.addWidget(QLabel(pixmap=QPixmap(food_paths[foodtype])))
                self.foodcostLayout.addWidget(QLabel(sep, styleSheet='font-weight: bold;'))
        self.foodcostLayout.removeItem(self.foodcostLayout.itemAt(self.foodcostLayout.count() - 1)) # remove trailing sep

        # Layout showing the chosen food to spend
        self.foodtospendLayout = QHBoxLayout()
        self.layout.addLayout(self.foodtospendLayout, 1, 0)
        # self.foodtospendLayout.addWidget(QLabel('Food to spend:', styleSheet='font-weight: bold;'))

        # Layout with buttons to add food to spend
        self.addfoodbuttonsLayout = QHBoxLayout()
        self.layout.addLayout(self.addfoodbuttonsLayout, 2, 0)
        invertBtn = QPushButton('Invertebrate')
        invertBtn.clicked.connect(lambda: self.addfoodtospend('Invertebrate'))
        self.addfoodbuttonsLayout.addWidget(invertBtn)
        seedBtn = QPushButton('Seed')
        seedBtn.clicked.connect(lambda: self.addfoodtospend('Seed'))
        self.addfoodbuttonsLayout.addWidget(seedBtn)
        rodentBtn = QPushButton('Rodent')
        rodentBtn.clicked.connect(lambda: self.addfoodtospend('Rodent'))
        self.addfoodbuttonsLayout.addWidget(rodentBtn)
        fishBtn = QPushButton('Fish')
        fishBtn.clicked.connect(lambda: self.addfoodtospend('Fish'))
        self.addfoodbuttonsLayout.addWidget(fishBtn)
        fruitBtn = QPushButton('Fruit')
        fruitBtn.clicked.connect(lambda: self.addfoodtospend('Fruit'))
        self.addfoodbuttonsLayout.addWidget(fruitBtn)

        # Accept / reject button box
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Reset)
        self.layout.addWidget(self.buttonBox, 3, 0)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.StandardButton.Reset).clicked.connect(self.resetfoodtospend)

    def addfoodtospend(self, foodtype):
        self.foodtospendLayout.addWidget(QLabel(pixmap=QPixmap(food_paths[foodtype])))
        self.foodtospend[foodtype] += 1

    def resetfoodtospend(self):
        clearLayout(self.foodtospendLayout)
        for k in self.foodtospend:
            self.foodtospend[k] = 0

    def get_inputs(self):
        return self.foodtospend