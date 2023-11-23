from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QHBoxLayout
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
        super().__init__()
        layout = QGridLayout()
        layout.addWidget(QLabel(birdcard.common_name, styleSheet='font-weight: bold;'), 0, 0)
        layout.addWidget(QLabel(f'VP: {birdcard.victory_points}, Wingspan: {birdcard.wingspan}'), 1, 0)
        
        foodLayout = QHBoxLayout()
        layout.addLayout(foodLayout, 2, 0, 1, 2)
        foods = [
            ('Invertebrate', birdcard.invertebrate), ('Seed', birdcard.seed), 
            ('Fish', birdcard.fish), ('Fruit', birdcard.fruit), ('Rodent', birdcard.rodent), 
            ('Wild', birdcard.wild_food)
        ]
        food_added = 0
        print(birdcard.slash_food_cost)
        sep = '/' if birdcard.slash_food_cost else '+'
        for food, num in foods:
            for i in range(num):
                foodLayout.addWidget(QLabel(pixmap=QPixmap(food_images[food])))
                food_added += 1
                if food_added < birdcard.total_food_cost:
                    foodLayout.addWidget(QLabel(sep, styleSheet='font-weight: bold;'))
        
        nestLayout = QHBoxLayout()
        layout.addLayout(nestLayout, 3, 0 , 1, 2)
        nestLayout.addWidget(QLabel(pixmap=QPixmap(nest_images[birdcard.nest_type])))
        for i in range(birdcard.laideggs):
            nestLayout.addWidget(QLabel(pixmap=QPixmap('./images/game_smallegg.png')))
        for i in range(birdcard.egg_capacity - birdcard.laideggs):
            nestLayout.addWidget(QLabel(pixmap=QPixmap('./images/game_egg.png')))

        layout.addWidget(QLabel(birdcard.power_text), 4, 0, 1, 2)
        
        self.setLayout(layout)
