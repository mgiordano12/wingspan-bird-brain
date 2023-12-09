from Power import Power
from PowerGainFood import *
from collections import defaultdict 

bird_power_dict = {
 'Gain 1 [fruit] from the supply.' : PowerGainFood('Fruit',1),
 'Gain 1 [invertebrate] from the supply.' : PowerGainFood('Invertebrate',1),
 'Gain 1 [seed] from the supply.' : PowerGainFood('Seed',1),
 'Gain 3 [fish] from the supply.' : PowerGainFood('Fish',3),
 'Gain 3 [seed] from the supply.' : PowerGainFood('Seed',3),
 'When another player plays a bird in their [forest], gain 1 [invertebrate] from the supply.' : PowerGainFood('Invertebrate',1),
 'When another player plays a bird in their [wetland], gain 1 [fish] from the supply.' : PowerGainFood('Fish',1)
}

# Until we have more powers implemented, initialize to the superclass Power
bird_power_dict = defaultdict(lambda: Power(), bird_power_dict)