import sys
sys.path.append('../')
from BirdCard import BirdCard
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QPixmap

food_images = {
    'Fish': './images/food_fish.png', 'Rodent': './images/food_rodent.png', 
    'Fruit': './images/food_fruit.png', 'Invertebrate': './images/food_invertebrate.png', 
    'Seed': './images/food_seed.png', 'Wild': './images/food_wild.png',
}
nest_images = {
    'Bowl': './images/nest_bowl.png', 'Cavity': './images/nest_cavity.png',
    'Ground': './images/nest_ground.png', 'Platform': './images/nest_platform.png',
    'Wild': './images/nest_star.png'
}

class BirdCardWidget(QWidget):

    def __init__(self, birdcard, **kwargs):
        if not isinstance(birdcard, BirdCard):
            raise TypeError('BirdCardWidget must be initialized with a BirdCard object.')
        super().__init__()
        layout = QVBoxLayout(self)

        # Name, VP, and wingspan
        layout.addWidget(QLabel(birdcard.common_name, styleSheet='font-weight: bold;'))
        layout.addWidget(QLabel(f'VP: {birdcard.victory_points}, Wingspan: {birdcard.wingspan} cm'))

        # Habitats
        habitatLayout = QHBoxLayout()
        layout.addLayout(habitatLayout)
        if birdcard.forest:
            habitatLayout.addWidget(QLabel(pixmap=QPixmap('./images/habitat_forest.png').scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)))
        if birdcard.grassland:
            habitatLayout.addWidget(QLabel(pixmap=QPixmap('./images/habitat_grassland.png').scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)))
        if birdcard.wetland:
            habitatLayout.addWidget(QLabel(pixmap=QPixmap('./images/habitat_wetland.png').scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)))
        
        # Food
        foodLayout = QHBoxLayout()
        layout.addLayout(foodLayout)
        foods = [
            ('Invertebrate', birdcard.invertebrate), ('Seed', birdcard.seed), 
            ('Fish', birdcard.fish), ('Fruit', birdcard.fruit), ('Rodent', birdcard.rodent), 
            ('Wild', birdcard.wild_food)
        ]
        food_added = 0
        sep = '/' if birdcard.slash_food_cost else '+' # food separator
        target = sum([num for _, num in foods]) # number of food tokens to be displayed
        for food, num in foods:
            for i in range(num):
                foodLayout.addWidget(QLabel(pixmap=QPixmap(food_images[food]).scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)))
                food_added += 1
                if food_added < target:
                    foodLayout.addWidget(QLabel(sep, styleSheet='font-weight: bold;'))
        
        # Nest and eggs
        nestLayout = QHBoxLayout()
        layout.addLayout(nestLayout)
        if birdcard.nest_type == 'None':
            nest = QLabel('None', styleSheet='border: 1px solid black;')
        else:
            nest = QLabel(pixmap=QPixmap(nest_images[birdcard.nest_type]).scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        nestLayout.addWidget(nest)
        for i in range(birdcard.laideggs):
            nestLayout.addWidget(QLabel(pixmap=QPixmap('./images/game_smallegg.png').scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)))
        for i in range(birdcard.egg_capacity - birdcard.laideggs):
            nestLayout.addWidget(QLabel(pixmap=QPixmap('./images/game_egg.png').scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)))

        # Power text
        layout.addWidget(QLabel(birdcard.power_text, wordWrap=True))
