import sys
sys.path.append('../')
from BirdCard import BirdCard
from PyQt6.QtWidgets import QGridLayout, QDialog, QLabel, QDialogButtonBox, QComboBox, QHBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

# Image paths for food
foodimages = {
    'Fish': './images/food_fish.png', 'Rodent': './images/food_rodent.png', 
    'Fruit': './images/food_fruit.png', 'Invertebrate': './images/food_invertebrate.png', 
    'Seed': './images/food_seed.png', 'Invertebrate+Seed': './images/food_invertebrate+seed.png',
    'Wild': './images/food_wild.png',
}

class SpendFoodPopup(QDialog):

    def __init__(self, card, foodinhand):
        """
        card is the card being played
        foodinhand is the food in the hand of the player trying to play the card
        """
        if type(card) is not BirdCard:
            raise Exception('`card` in SpendFoodPopup.__init__() must be of type BirdCard')
        if type(foodinhand) is not dict:
            raise Exception('`foodinhand` must be a dict')
        
        super().__init__()

        self.layout = QGridLayout(self)

        self.renderfoodinhand(foodinhand)

        # Create food cost column
        nrows = 1
        self.foodcost = list()
        cardfoods = [('Invertebrate', card.invertebrate), ('Seed', card.seed), 
                     ('Fruit', card.fruit), ('Fish', card.fish), 
                     ('Rodent', card.rodent), ('Wild', card.wild_food)]
        if card.slash_food_cost:
            # Create sublayout with all of the slash food options
            l = QHBoxLayout()
            for foodtype, cnt in cardfoods:
                if cnt > 0:
                    l.addWidget(QLabel(pixmap=QPixmap(foodimages[foodtype])))
                    l.addWidget(QLabel('/', styleSheet='font-weight: bold;'))
                    self.foodcost.append(foodtype)
            l.removeItem(l.itemAt(l.count() - 1)) # remove trailing slash
            self.layout.addLayout(l, nrows, 0) # add slash food cost layout to main layout
            # Create dropdown
            w = QComboBox()
            w.addItem('None')
            for f in foodinhand:
                if foodinhand[f] > 0:
                    w.addItem(f)
            # w.currentIndexChanged.connect(self.dropdownChanged)
            self.layout.addWidget(w, nrows, 1)
            nrows += 1
        else:
            for foodtype, cnt in cardfoods:
                for i in range(cnt):
                    self.layout.addWidget(QLabel(pixmap=QPixmap(foodimages[foodtype])), nrows, 0)
                    self.foodcost.append(foodtype)
                    w1, w2 = QComboBox(), QComboBox()
                    w1.addItem('None')
                    w2.addItem('None')
                    for f in foodinhand:
                        if foodinhand[f] > 0:
                            w1.addItem(f)
                            w2.addItem(f)
                    # w1.currentIndexChanged.connect(self.dropdownChanged)
                    # w2.currentIndexChanged.connect(self.dropdownChanged)
                    self.layout.addWidget(w1, nrows, 1)
                    self.layout.addWidget(w2, nrows, 2)
                    nrows += 1

        # Accept / reject button box
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonBox, nrows, 2)

    def renderfoodinhand(self, food):
        foodHandLayout = QGridLayout()
        foodHandLayout.addWidget(QLabel('Food in hand: ', styleSheet='font-weight: bold;'), 0, 0)
        foodHandLayout.addWidget(QLabel(pixmap=QPixmap('./images/food_invertebrate.png').scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)), 0, 1)
        foodHandLayout.addWidget(QLabel(f'x {food["Invertebrate"]}'), 0, 2)
        foodHandLayout.addWidget(QLabel(pixmap=QPixmap('./images/food_seed.png').scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)), 0, 3)
        foodHandLayout.addWidget(QLabel(f'x {food["Seed"]}'), 0, 4)
        foodHandLayout.addWidget(QLabel(pixmap=QPixmap('./images/food_fish.png').scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)), 0, 5)
        foodHandLayout.addWidget(QLabel(f'x {food["Fish"]}'), 0, 6)
        foodHandLayout.addWidget(QLabel(pixmap=QPixmap('./images/food_rodent.png').scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)), 0, 7)
        foodHandLayout.addWidget(QLabel(f'x {food["Rodent"]}'), 0, 8)
        foodHandLayout.addWidget(QLabel(pixmap=QPixmap('./images/food_fruit.png').scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)), 0, 9)
        foodHandLayout.addWidget(QLabel(f'x {food["Fruit"]}'), 0, 10)
        self.layout.addLayout(foodHandLayout, 0, 0, 1, 3)

    def get_inputs(self):
        return -1
    
    def dropdownChanged(self):
        for r in range(self.layout.rowCount()-1):
            foodtype = self.foodcost[r]
            print(foodtype)
            # combobox1 = self.layout.itemAtPosition(r, 1).widget()
            # combobox2 = self.layout.itemAtPosition(r, 2).widget()