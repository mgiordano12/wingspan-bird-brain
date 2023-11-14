from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QGridLayout, QLabel, QWidget, QHBoxLayout, 
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
        self.turnsRemainingLayout = QGridLayout()
        self.forestLayout = QHBoxLayout()
        self.grasslandLayout = QHBoxLayout()
        self.wetlandLayout = QHBoxLayout()
        self.eorgLayout = QGridLayout()
        self.birdfeederLayout = QGridLayout()
        self.cardLayout = QGridLayout()

        # Turns remaining layout
        self.turnsRemainingLayout.addWidget(QLabel('Round: 1'))
        self.turnsRemainingLayout.addWidget(QLabel('Turns remaining: 8'))

        # Forest habitat layout
        forestBox1 = QLabel(styleSheet='border: 1px solid black;')
        forestBox2 = QLabel(styleSheet='border: 1px solid black;')
        forestBox3 = QLabel(styleSheet='border: 1px solid black;')
        forestBox4 = QLabel(styleSheet='border: 1px solid black;')
        forestBox5 = QLabel(styleSheet='border: 1px solid black;')
        forestBox6 = QLabel(styleSheet='border: 1px solid black;')
        self.forestLayout.addWidget(QLabel(pixmap=QPixmap('./images/habitat_forest.png')))
        self.forestLayout.addWidget(forestBox1)
        self.forestLayout.addWidget(forestBox2)
        self.forestLayout.addWidget(forestBox3)
        self.forestLayout.addWidget(forestBox4)
        self.forestLayout.addWidget(forestBox5)
        self.forestLayout.addWidget(forestBox6)

        # Grassland habitat
        grasslandBox1 = QLabel(styleSheet='border: 1px solid black;')
        grasslandBox2 = QLabel(styleSheet='border: 1px solid black;')
        grasslandBox3 = QLabel(styleSheet='border: 1px solid black;')
        grasslandBox4 = QLabel(styleSheet='border: 1px solid black;')
        grasslandBox5 = QLabel(styleSheet='border: 1px solid black;')
        grasslandBox6 = QLabel(styleSheet='border: 1px solid black;')
        self.grasslandLayout.addWidget(QLabel(pixmap=QPixmap('./images/habitat_grassland.png')))
        self.grasslandLayout.addWidget(grasslandBox1)
        self.grasslandLayout.addWidget(grasslandBox2)
        self.grasslandLayout.addWidget(grasslandBox3)
        self.grasslandLayout.addWidget(grasslandBox4)
        self.grasslandLayout.addWidget(grasslandBox5)
        self.grasslandLayout.addWidget(grasslandBox6)

        # Wetland habitat
        wetlandBox1 = QLabel(styleSheet='border: 1px solid black;')
        wetlandBox2 = QLabel(styleSheet='border: 1px solid black;')
        wetlandBox3 = QLabel(styleSheet='border: 1px solid black;')
        wetlandBox4 = QLabel(styleSheet='border: 1px solid black;')
        wetlandBox5 = QLabel(styleSheet='border: 1px solid black;')
        wetlandBox6 = QLabel(styleSheet='border: 1px solid black;')
        self.wetlandLayout.addWidget(QLabel(pixmap=QPixmap('./images/habitat_wetland.png')))
        self.wetlandLayout.addWidget(wetlandBox1)
        self.wetlandLayout.addWidget(wetlandBox2)
        self.wetlandLayout.addWidget(wetlandBox3)
        self.wetlandLayout.addWidget(wetlandBox4)
        self.wetlandLayout.addWidget(wetlandBox5)
        self.wetlandLayout.addWidget(wetlandBox6)

        # EORG Layout
        self.eorgLayout.addWidget(QLabel('End of Round Goals'), 0, 0)
        self.eorgLayout.addWidget(QLabel('Rd. 1'), 1, 0)
        self.eorgLayout.addWidget(QLabel('Rd. 2'), 1, 1)
        self.eorgLayout.addWidget(QLabel('Rd. 3'), 1, 2)
        self.eorgLayout.addWidget(QLabel('Rd. 4'), 1, 3)
        self.eorgLayout.addWidget(QLabel(styleSheet='border: 1px solid black;'), 2, 0)
        self.eorgLayout.addWidget(QLabel(styleSheet='border: 1px solid black;'), 2, 1)
        self.eorgLayout.addWidget(QLabel(styleSheet='border: 1px solid black;'), 2, 2)
        self.eorgLayout.addWidget(QLabel(styleSheet='border: 1px solid black;'), 2, 3)

        # Birdfeeder Layout
        self.birdfeederLayout.addWidget(QLabel('In feeder:'), 0, 0)
        self.birdfeederLayout.addWidget(QLabel(styleSheet='border: 1px solid black;'), 1, 0)
        self.birdfeederLayout.addWidget(QLabel(styleSheet='border: 1px solid black;'), 2, 0)
        self.birdfeederLayout.addWidget(QLabel(styleSheet='border: 1px solid black;'), 3, 0)
        self.birdfeederLayout.addWidget(QLabel(styleSheet='border: 1px solid black;'), 4, 0)
        self.birdfeederLayout.addWidget(QLabel(styleSheet='border: 1px solid black;'), 5, 0)
        self.birdfeederLayout.addWidget(QLabel('Out of feeder:'), 0, 1)
        self.birdfeederLayout.addWidget(QLabel(styleSheet='border: 1px solid black;'), 1, 1)
        self.birdfeederLayout.addWidget(QLabel(styleSheet='border: 1px solid black;'), 2, 1)
        self.birdfeederLayout.addWidget(QLabel(styleSheet='border: 1px solid black;'), 3, 1)
        self.birdfeederLayout.addWidget(QLabel(styleSheet='border: 1px solid black;'), 4, 1)
        self.birdfeederLayout.addWidget(QLabel(styleSheet='border: 1px solid black;'), 5, 1)

        # Card Layout
        self.cardLayout.addWidget(QLabel('Bird cards'), 0, 0)
        self.cardLayout.addWidget(QLabel(styleSheet='border: 1px solid black;'), 0, 1)
        self.cardLayout.addWidget(QLabel(styleSheet='border: 1px solid black;'), 1, 0)
        self.cardLayout.addWidget(QLabel(styleSheet='border: 1px solid black;'), 1, 1)
        self.cardLayout.addWidget(QLabel(styleSheet='border: 1px solid black;'), 1, 2)
        
        # Add layouts to central layout
        self.centralLayout.addLayout(self.turnsRemainingLayout, 0, 0)
        self.centralLayout.addLayout(self.forestLayout, 1, 0)
        self.centralLayout.addLayout(self.grasslandLayout, 2, 0)
        self.centralLayout.addLayout(self.wetlandLayout, 3, 0)
        self.centralLayout.addLayout(self.eorgLayout, 0, 1)
        self.centralLayout.addLayout(self.birdfeederLayout, 1, 1)
        self.centralLayout.addLayout(self.cardLayout, 2, 1)

        w = QWidget()
        w.setLayout(self.centralLayout)
        self.setCentralWidget(w)

# Main loop ====================================================================
app = QApplication(sys.argv)
window = WingspanAppWindow() 
window.show()
app.exec() # start event loop
