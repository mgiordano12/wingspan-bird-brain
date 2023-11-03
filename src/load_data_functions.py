from BirdCard import BirdCard
from BonusCard import BonusCard
from EndOfRoundGoal import EndOfRoundGoal
import json
import requests

#=======================================================================================================================
def load_birdcards():
    birdcard_dicts = json.loads(requests.get("https://raw.githubusercontent.com/navarog/wingsearch/master/src/assets/data/master.json").content)
    birdcard_objs = list()
    for i in birdcard_dicts:
        bird = BirdCard(
            common_name = i["Common name"],
            scientific_name=i["Scientific name"],
            expansion=i["Expansion"],
            color=i["Color"],
            power_category=i["PowerCategory"],
            power_text=i["Power text"],
            predator=True if i["Predator"]=="X" else False,
            flocking=True if i["Flocking"]=="X" else False,
            bonus_card=True if i["Bonus card"]=="X" else False,
            victory_points=int(i["Victory points"]),
            nest_type=i["Nest type"],
            egg_capacity=int(i["Egg capacity"]),
            wingspan=int(i["Wingspan"]) if i["Wingspan"]!="*" else None,
            forest=True if i["Forest"]=="X" else False,
            grassland=True if i["Grassland"]=="X" else False,
            wetland=True if i["Wetland"]=="X" else False,
            invertebrate=0 if i["Invertebrate"] is None else int(i["Invertebrate"]),
            seed=0 if i["Seed"] is None else int(i["Seed"]),
            fish=0 if i["Fish"] is None else int(i["Fish"]),
            fruit=0 if i["Fruit"] is None else int(i["Fruit"]),
            rodent=0 if i["Rodent"] is None else int(i["Rodent"]),
            nectar=0 if i["Nectar"] is None else int(i["Nectar"]),
            wild_food=0 if i["Wild (food)"] is None else int(i["Wild (food)"]),
            slash_food_cost=True if i["/ (food cost)"]=="X" else False,
            asterisk_food_cost=True if i["* (food cost)"]=="X" else False,
            total_food_cost=int(i["Total food cost"]),
            anatomist=True if i["Anatomist"]=="X" else False, 
            cartographer=True if i["Cartographer"]=="X" else False, 
            historian=True if i["Historian"]=="X" else False, 
            photographer=True if i["Photographer"]=="X" else False, 
            backyard_birder=True if i["Backyard Birder"]=="X" else False, 
            bird_bander=True if i["Bird Bander"]=="X" else False, 
            bird_counter=True if i["Bird Counter"]=="X" else False, 
            bird_feeder=True if i["Bird Feeder"]=="X" else False, 
            diet_specialist=True if i["Diet Specialist"]=="X" else False, 
            enclosure_builder=True if i["Enclosure Builder"]=="X" else False, 
            falconer=True if i["Falconer"]=="X" else False, 
            fishery_manager=True if i["Fishery Manager"]=="X" else False, 
            food_web_expert=True if i["Food Web Expert"]=="X" else False, 
            forester=True if i["Forester"]=="X" else False, 
            large_bird_specialist=True if i["Large Bird Specialist"]=="X" else False, 
            nest_box_builder=True if i["Nest Box Builder"]=="X" else False, 
            omnivore_expert=True if i["Omnivore Expert"]=="X" else False, 
            passerine_specialist=True if i["Passerine Specialist"]=="X" else False, 
            platform_builder=True if i["Platform Builder"]=="X" else False, 
            prairie_manager=True if i["Prairie Manager"]=="X" else False, 
            rodentologist=True if i["Rodentologist"]=="X" else False, 
            viticulturalist=True if i["Viticulturalist"]=="X" else False, 
            wetland_scientist=True if i["Wetland Scientist"]=="X" else False, 
            wildlife_gardener=True if i["Wildlife Gardener"]=="X" else False,
            caprimulgiform_specialist=True if i["Caprimulgiform Specialist"]=="X" else False, 
            small_clutch_specialist=True if i["Small Clutch Specialist"]=="X" else False, 
            endangered_species_protector=True if i["Endangered Species Protector"]=="X" else False, 
            beak_pointing_left=True if i["Beak Pointing Left"]=="X" else False, 
            beak_pointing_right=True if i["Beak Pointing Right"]=="X" else False, 
            note=i["Note"], 
            id=int(i["id"]), 
            rulings=i["rulings"], 
            additional_rulings=i['additionalRulings'],
        )
        birdcard_objs.append(bird)
    return birdcard_objs

#=======================================================================================================================
def load_endofroundgoals():
    goals_dicts = json.loads(requests.get("https://raw.githubusercontent.com/navarog/wingsearch/master/src/assets/data/goals.json").content)
    goals_objs = list()
    for i in goals_dicts:
        goal = EndOfRoundGoal(
            name=i["Name"],
            expansion=i["Expansion"],
            duet=True if i["Duet"]=="X" else False,
            condition=i["Condition"],
            explanatory_text=i["Explanatory Text"],
            id=int(i["id"]),
        )
        goals_objs.append(goal)
    return goals_objs

#=======================================================================================================================
def load_bonuses():
    bonus_dicts = json.loads(requests.get("https://raw.githubusercontent.com/navarog/wingsearch/master/src/assets/data/bonus.json").content)
    bonus_objs = list()
    for i in bonus_dicts:
        bonus = BonusCard(
            name=i["Name"],
            expansion=i["Expansion"],
            automa=True if i["Automa"]=="X" else False,
            condition=i["Condition"],
            explanatory_text=i["Explanatory text"],
            vp=i["VP"],
            percent=int(i["%"]) if type(i["%"]) is int else None,
            note=i["Note"],
            vp_average=float(i["VP Average"]),
            id=i["id"],
            rulings=i["rulings"],
        )
        bonus_objs.append(bonus)
    return bonus_objs