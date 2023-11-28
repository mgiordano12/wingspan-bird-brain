from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class BonusCardWidget(QWidget):
    def __init__(self, bonuscard):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(bonuscard.name, styleSheet='font-weight: bold;'))
        layout.addWidget(QLabel(bonuscard.condition, wordWrap=True))
        layout.addWidget(QLabel(bonuscard.vp, wordWrap=True))
        layout.addWidget(QLabel(f'{bonuscard.percent}% of cards'))
        self.styleSheet = 'border: 1px solid black;'