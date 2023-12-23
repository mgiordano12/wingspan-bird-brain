import sys
sys.path.append('../')
from BirdCardWidget import BirdCardWidget
from BonusCardWidget import BonusCardWidget
from PyQt6.QtWidgets import QGridLayout, QDialog, QListWidget, QAbstractItemView, QDialogButtonBox

class StartingMaterialsPopup(QDialog):
    def __init__(self, birdcards, bonuscards):
        super().__init__()
        self.birdcards = birdcards
        self.bonuscards = bonuscards
        layout = QGridLayout(self)
        layout.addWidget(BirdCardWidget(birdcards[0]), 0, 0)
        layout.addWidget(BirdCardWidget(birdcards[1]), 0, 1)
        layout.addWidget(BirdCardWidget(birdcards[2]), 0, 2)
        layout.addWidget(BirdCardWidget(birdcards[3]), 0, 3)
        layout.addWidget(BirdCardWidget(birdcards[4]), 0, 4)
        layout.addWidget(BonusCardWidget(bonuscards[0]), 1, 0)
        layout.addWidget(BonusCardWidget(bonuscards[1]), 1, 1)
        
        self.birdCardSelect = QListWidget(selectionMode=QAbstractItemView.SelectionMode.MultiSelection)
        for card in birdcards:
            self.birdCardSelect.addItem(card.common_name)
        layout.addWidget(self.birdCardSelect, 1, 2)
        
        self.bonusCardSelect = QListWidget(selectionMode=QAbstractItemView.SelectionMode.MultiSelection)
        for card in bonuscards:
            self.bonusCardSelect.addItem(card.name)
        layout.addWidget(self.bonusCardSelect, 1, 3)
        
        self.foodSelect = QListWidget(selectionMode=QAbstractItemView.SelectionMode.MultiSelection)
        self.foodSelect.addItems(['Invertebrate', 'Seed', 'Fruit', 'Fish', 'Rodent'])
        layout.addWidget(self.foodSelect, 1, 4)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox, 2, 4)

    def getInputs(self):
        birdcards = [
            c for item in self.birdCardSelect.selectedItems() 
            for c in self.birdcards if c.common_name==item.text()
        ]
        bonuscards = [
            c for item in self.bonusCardSelect.selectedItems() 
            for c in self.bonuscards if c.name==item.text()
        ]
        foods = [item.text() for item in self.foodSelect.selectedItems()]
        return birdcards, bonuscards, foods