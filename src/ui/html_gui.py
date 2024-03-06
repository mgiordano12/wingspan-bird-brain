from BirdCard import BirdCard
from BonusCard import BonusCard
from Birdfeeder import Birdfeeder
from Player import Player
from BirdCardDeck import BirdCardDeck
from EndOfRoundGoalMat import EndOfRoundGoalMat
from imagepaths import habitat_paths, food_paths, nest_paths, eorg_paths
from load_data_functions import load_birdcards, load_bonuses
from Gameplay_Constants import FOOD_TYPES, BIRDCARD_FOOD_MAPPING, BIRDFEEDER_FACES

from xml.dom.minidom import getDOMImplementation, parseString
import os
from textwrap import wrap
import base64

#=======================================================================================================================
def createImgTag(src, width=20, height=20, style=''):
    # Convert src from path to base64 byte string
    with open(src, 'rb') as f:
        src = base64.b64encode(f.read()).decode()
    return parseString(f'<img src="data:image/png;base64,{src}" width="{width}" height="{height}" style="{style}"></img>').documentElement

#=======================================================================================================================
def createBirdCardDiv(birdcard):
    assert type(birdcard) is BirdCard

    topDiv = parseString(f'''
        <div class="birdcard" style="border: 1px solid gray; font-family: sans-serif; font-weight: bold; display: inline-block;"> 
            <u>{birdcard.common_name}</u> 
        </div>
    ''').documentElement
    topDiv.appendChild(parseString(f'''
        <div class="bird info" style="font-weight: normal;">
            VP: {birdcard.victory_points}, Wingspan: {birdcard.wingspan}
        </div>
    ''').documentElement)

    # Habitats
    habitatDiv = parseString('<div class="habitats"></div>').documentElement
    if birdcard.forest:
        habitatDiv.appendChild(createImgTag(habitat_paths['Forest']))
    if birdcard.grassland:
        habitatDiv.appendChild(createImgTag(habitat_paths['Grassland']))
    if birdcard.wetland:
        habitatDiv.appendChild(createImgTag(habitat_paths['Wetland']))
    topDiv.appendChild(habitatDiv)

    # Food Cost
    sep = '/' if birdcard.slash_food_cost else '+'
    totalFoodCost = birdcard.total_food_cost
    foodAdded = 0
    foodCostDiv = parseString('<div class="foodCost" style="display: flex;"></div>').documentElement
    for food in FOOD_TYPES:
        cnt = birdcard.__dict__[BIRDCARD_FOOD_MAPPING[food]]
        for _ in range(cnt):
            foodCostDiv.appendChild(createImgTag(food_paths[food]))
            foodAdded += 1
            if foodAdded < totalFoodCost:
                # foodCostDiv.appendChild(doc.createTextNode(sep))
                foodCostDiv.appendChild(parseString(f'<div>{sep}</div>').documentElement)
    topDiv.appendChild(foodCostDiv)

    # Nest type and eggs
    nestDiv = parseString('<div class="nest"></div>').documentElement
    nestDiv.appendChild(createImgTag(nest_paths[birdcard.nest_type]))
    for _ in range(birdcard.laideggs):
        nestDiv.appendChild(createImgTag(os.path.abspath('./ui/images/game_egg.png'), height=25, width=25))
    for _ in range(birdcard.egg_capacity - birdcard.laideggs):
        nestDiv.appendChild(createImgTag(os.path.abspath('./ui/images/game_smallegg.png')))
    topDiv.appendChild(nestDiv)

    # Power text
    topDiv.appendChild(parseString(f'<div class="power text" style="font-weight: normal;">{birdcard.power_text}</div>').documentElement)

    return topDiv

#=======================================================================================================================
def createBonusCardDiv(bonuscard):
    assert type(bonuscard) is BonusCard
    
    topDiv = parseString(f'''
        <div class="bonuscard" style="border: 1px solid black; font-family: sans-serif; display: inline-block; text-align: center;"> 
            <b><u>{bonuscard.name}</u></b><br></br>
            {'<br></br>'.join(wrap(bonuscard.condition, 40))}<br></br>
            {'<br></br>'.join(wrap(bonuscard.explanatory_text, 40))}<br></br>
            {bonuscard.vp}<br></br>
            {bonuscard.percent}% of cards<br></br>
        </div>
    ''').documentElement

    return topDiv

#=======================================================================================================================
def createBirdfeederDiv(birdfeeder):
    assert type(birdfeeder) is Birdfeeder

    topDiv = parseString('<div class="birdfeeder" style="display: flex;"></div>').documentElement
    inFeederDiv = parseString('<div class="infeeder" style="border: 2px solid black;"></div>').documentElement
    topDiv.appendChild(inFeederDiv)
    for dice in birdfeeder.food:
        inFeederDiv.appendChild(createImgTag(food_paths[dice], width=40, height=40, style='border: 1px dotted gray'))
    outOfFeederDiv = parseString('<div class="outoffeeder"></div>').documentElement
    topDiv.appendChild(outOfFeederDiv)
    for _ in range(5-len(birdfeeder.food)):
        outOfFeederDiv.appendChild(createImgTag(os.path.abspath('./ui/images/game_die.png'), height=40, width=40))

    return topDiv

#=======================================================================================================================
def createHabitatDiv(player, habitat):
    assert habitat in ['forest', 'grassland', 'wetland']
    assert type(player) is Player

    topDiv = parseString(f'<div class="{habitat}" style="font-family: sans-serif; display: flex; border: 1px solid black"></div>').documentElement
    topDiv.appendChild(parseString(f'''
        <div style="display: inline-block"> 
            <b>{habitat.upper()}</b> 
            {createImgTag(habitat_paths[habitat.capitalize()], height=40, width=40).toxml()} 
        </div>
    ''').documentElement)
    playerHab = player.gamemat.habitats[habitat]
    for card in playerHab:
        topDiv.appendChild(createBirdCardDiv(card))
        
    return topDiv

#=======================================================================================================================
def createFaceUpBirdCardDiv(birddeck):
    assert type(birddeck) is BirdCardDeck
    topDiv = parseString('<div class="birddeck" style="display: flex;"></div>').documentElement
    for card in birddeck.faceup_cards:
        topDiv.appendChild(createBirdCardDiv(card))
    return topDiv

#=======================================================================================================================
def createGameInfoDiv(round, turn, eorgMat):
    assert type(round) is int
    assert type(turn) is int
    assert type(eorgMat) is EndOfRoundGoalMat

    topDiv = parseString(f'''
        <div class="game-info" style="font-family: sans-serif;">
            <b>Round: {round}, Turn: {turn}</b>
        </div>
    ''').documentElement

    eorgDiv = parseString('<div style="display: flex;"></div>').documentElement
    topDiv.appendChild(eorgDiv)
    for i, goal in enumerate(eorgMat.goals):
        eorgDiv.appendChild(parseString(f'''
            <div> 
                Round {4-i}: 
                {createImgTag(eorg_paths[goal.name], height=60, width=60).toxml()}
                <span style="display:inline-block; width: 30;"></span>
            </div>
        ''').documentElement)

    return topDiv

#=======================================================================================================================
def createFoodInHandDiv(player):
    assert type(player) is Player

    topDiv = parseString('<div class="food-in-hand" style="font-family: sans-serif; display: flex;"></div>').documentElement

    for food, cnt in player.food.items():
        topDiv.appendChild(parseString(f'''
            <div>
                {createImgTag(food_paths[food], height=40, width=40).toxml()} x {cnt}
            </div>
        ''').documentElement)

    return topDiv

#=======================================================================================================================
def createBirdsInHandDiv(player):
    assert type(player) is Player
    topDiv = parseString(f'<div class="birds-in-hand" style="display: wrap;"></div>').documentElement
    for card in player.birdcards:
        topDiv.appendChild(createBirdCardDiv(card))
    return topDiv

#=======================================================================================================================
def createBonusInHandDiv(player):
    assert type(player) is Player
    topDiv = parseString(f'<div class="bonus-in-hand" style="display: wrap;"></div>').documentElement
    for card in player.bonuscards:
        topDiv.appendChild(createBonusCardDiv(card))
    return topDiv

#=======================================================================================================================
def createHTML(round, turn, eorgMat, player, birdfeeder, birddeck):
    impl = getDOMImplementation()
    doc = impl.createDocument(None, 'gui', None)
    html = doc.documentElement

    html.appendChild(createGameInfoDiv(round, turn, eorgMat)) # game info

    html.appendChild(parseString('<div style="font-family: sans-serif; font-size: 28px"> <b><u><i>Habitats</i></u></b> </div>').documentElement)

    html.appendChild(createHabitatDiv(player, 'forest')) # habitats
    html.appendChild(createHabitatDiv(player, 'grassland'))
    html.appendChild(createHabitatDiv(player, 'wetland'))

    html.appendChild(parseString('<div style="font-family: sans-serif; font-size: 28px"> <b><u><i>Birdfeeder</i></u></b> </div>').documentElement)
    html.appendChild(createBirdfeederDiv(birdfeeder)) # birdfeeder

    html.appendChild(parseString('<div style="font-family: sans-serif; font-size: 28px"> <b><u><i>Face-up Bird Cards</i></u></b> </div>').documentElement)
    html.appendChild(createFaceUpBirdCardDiv(birddeck)) # face up bird cards

    html.appendChild(parseString('<div style="font-family: sans-serif; font-size: 28px"> <b><u><i>Food in hand</i></u></b> </div>').documentElement)
    html.appendChild(createFoodInHandDiv(player)) # things player has
    html.appendChild(parseString('<div style="font-family: sans-serif; font-size: 28px"> <b><u><i>Birds in hand</i></u></b> </div>').documentElement)
    html.appendChild(createBirdsInHandDiv(player))
    html.appendChild(parseString('<div style="font-family: sans-serif; font-size: 28px"> <b><u><i>Bonuses in hand</i></u></b> </div>').documentElement)
    html.appendChild(createBonusInHandDiv(player))

    return doc.toxml()