class BirdCard:

    #===================================================================================================================
    def __init__(
            self, common_name, scientific_name, expansion, color, power_category, power_text, predator, flocking, 
            bonus_card, victory_points, nest_type, egg_capacity, wingspan, forest, grassland, wetland, invertebrate, 
            seed, fish, fruit, rodent, nectar, wild_food, slash_food_cost, asterisk_food_cost, total_food_cost, 
            anatomist, cartographer, historian, photographer, backyard_birder, bird_bander, bird_counter, bird_feeder, 
            diet_specialist, enclosure_builder, falconer, fishery_manager, food_web_expert, forester, 
            large_bird_specialist, nest_box_builder, omnivore_expert, passerine_specialist, platform_builder, 
            prairie_manager, rodentologist, viticulturalist, wetland_scientist, wildlife_gardener, 
            caprimulgiform_specialist, small_clutch_specialist, endangered_species_protector, beak_pointing_left, 
            beak_pointing_right, note, id, rulings, additional_rulings,
        ):
        # General
        self.common_name = common_name
        self.scientific_name = scientific_name
        self.expansion = expansion
        self.color = color
        self.victory_points = victory_points
        self.wingspan = wingspan
        self.note = note
        self.id = id
        # Power
        self.power_category = power_category
        self.power_text = power_text
        self.predator = predator # predator power (om nom nom)
        self.flocking = flocking # flocking power (tuck other cards)
        self.bonus_card = bonus_card # bonus card power (draw more bonus cards)
        # Nest
        self.nest_type = nest_type
        self.egg_capacity = egg_capacity
        # Habitat
        self.forest = forest
        self.grassland = grassland
        self.wetland = wetland
        # Food Cost
        self.invertebrate = invertebrate
        self.seed = seed
        self.fish = fish
        self.fruit = fruit
        self.rodent = rodent
        self.nectar = nectar
        self.wild_food = wild_food # wildcard food type
        self.slash_food_cost = slash_food_cost # for food type ORs
        self.asterisk_food_cost = asterisk_food_cost # idk what this is for
        self.total_food_cost = total_food_cost
        # Bonus cards
        self.anatomist = anatomist
        self.cartographer = cartographer
        self.historian = historian
        self.photographer = photographer
        self.backyard_birder = backyard_birder
        self.bird_bander = bird_bander
        self.bird_counter = bird_counter
        self.bird_feeder = bird_feeder
        self.diet_specialist = diet_specialist
        self.enclosure_builder = enclosure_builder
        self.falconer = falconer
        self.fishery_manager = fishery_manager
        self.food_web_expert = food_web_expert
        self.forester = forester
        self.large_bird_specialist = large_bird_specialist
        self.nest_box_builder = nest_box_builder
        self.omnivore_expert = omnivore_expert
        self.passerine_specialist = passerine_specialist
        self.platform_builder = platform_builder
        self.prairie_manager = prairie_manager
        self.rodentologist = rodentologist
        self.viticulturalist = viticulturalist
        self.wetland_scientist = wetland_scientist
        self.wildlife_gardener = wildlife_gardener
        self.caprimulgiform_specialist = caprimulgiform_specialist
        self.small_clutch_specialist = small_clutch_specialist
        self.endangered_species_protector = endangered_species_protector
        # End of Round Goals
        self.beak_pointing_left = beak_pointing_left
        self.beak_pointing_right = beak_pointing_right
        # Rulings
        self.rulings = rulings
        self.additional_rulings = additional_rulings

        # For cards in play
        self.tuckedcards = 0
        self.cachedfood = 0
        self.laideggs = 0

    #===================================================================================================================
    def __repr__(self):
        return f"{self.common_name}"
    # include , Eggs: {self.laideggs}/{self.egg_capacity}, Nest: {self.nest_type}, Power: {self.victory_points}?