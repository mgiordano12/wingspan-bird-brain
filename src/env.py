import sys
sys.path.append('./ui/')
from pettingzoo import AECEnv
import functools
from copy import copy
from Game import Game
from Gameplay_Constants import NUMBER_OF_TURNS, BIRDFEEDER_FACES, NUMBER_BIRD_CARDS, MAX_NUMBER_DIE_IN_BIRDFEEDER, FOOD_TYPES
import datetime
import os
from html_gui import createHTML
import pickle
import gymnasium
from gymnasium.spaces import Discrete, MultiDiscrete, Box, MultiBinary
from gymnasium.spaces.utils import flatten_space
import numpy as np

class WingspanEnvironment(AECEnv):
    """ 
    The metadata holds environment constants. 
    """
    metadata = {
        "name": "WingspanEnvironment",
        "render_modes": ["human", "ansi",],
    }

    #===================================================================================================================
    def __init__(self, render_mode, log):
        """ 
        The init method takes in environment arguments and
         should define the following attributes:
        - possible_agents
        - render_mode
        """
        if render_mode not in self.metadata["render_modes"]:
            raise ValueError(f"`render_mode` must be in {self.metadata['render_modes']}")
        self.agents = ["birdbrain_0",]
        self.possible_agents = self.agents[:]
        self.render_mode = render_mode
        self.log = log

        self.observation_spaces = {
            a: gymnasium.spaces.Dict({
                "observation": gymnasium.spaces.Dict({
                    # 0=Fish, 1=Rodent, 2=Fruit, 3=Invertebrate, 4=Seed, 5=Invertebrate+seed, 6=dieOutOfFeeder
                    # +1 for die out of feeder
                    "Birdfeeder" : MultiDiscrete([len(BIRDFEEDER_FACES)+1,]*MAX_NUMBER_DIE_IN_BIRDFEEDER),
                }),
                "action_mask": gymnasium.spaces.Dict({
                    "Gain Food": Box(low=0, high=1, shape=(7,), dtype="int8"),
                    "Reroll Birdfeeder": Box(low=0, high=1, shape=(1,), dtype="int8"),
                })
            })
            for a in self.agents
        }
        self.action_spaces = {
            a: gymnasium.spaces.Dict({
                "Gain Food" : Discrete(7),
                "Reroll Birdfeeder": MultiBinary(1),
            })
            for a in self.agents
        }
        self.action_descriptions = {
            "Gain Food": [
                "Take Fish", "Take Rodent", "Take Fruit", "Take Invertebrate",
                "Take Seed", "Take Invert+Seed, gain Invertebrate", 
                "Take Invert+Seed, gain Seed",
            ],
            "Reroll Birdfeeder": ["Reroll Birdfeeder",],
        }
    #===================================================================================================================
    # lru_cache allows observation and action spaces to be memoized, reducing clock cycles required to get each agent's space.
    # If your spaces change over time, remove this line (disable caching).
    # @functools.lru_cache(maxsize=None)
    def observation_space(self, agent):
        return self.observation_spaces[agent]

    #===================================================================================================================
    # If your spaces change over time, remove this line (disable caching).
    # @functools.lru_cache(maxsize=None)
    def action_space(self, agent):
        return self.action_spaces[agent]
    
    #===================================================================================================================
    def observe(self, agent):
        """
        Should return the observations in action mask for the agent
        """
        observation = {
            "Birdfeeder": [
                np.argwhere(np.array(BIRDFEEDER_FACES)==self.game.birdfeeder.food[i])[0][0] if i < len(self.game.birdfeeder.food) else 6
                for i in range(MAX_NUMBER_DIE_IN_BIRDFEEDER)
            ]
        }

        action_mask = {
            "Gain Food": np.array(
                [
                    1 if "Fish" in self.game.birdfeeder.food else 0,
                    1 if "Rodent" in self.game.birdfeeder.food else 0,
                    1 if "Fruit" in self.game.birdfeeder.food else 0,
                    1 if "Invertebrate" in self.game.birdfeeder.food else 0,
                    1 if "Seed" in self.game.birdfeeder.food else 0,
                    1 if "Invertebrate+Seed" in self.game.birdfeeder.food else 0, # gain invert
                    1 if "Invertebrate+Seed" in self.game.birdfeeder.food else 0, # gain seed
                ], 
                dtype="int8"
            ),
            "Reroll Birdfeeder": np.array([self.game.birdfeeder.can_be_rerolled,], dtype="int8")
        }
    #===================================================================================================================
    def reset(self, seed=None, options=None):
        """
        Reset needs to initialize the following attributes
        - agents
        - rewards
        - _cumulative_rewards
        - terminations
        - truncations
        - infos
        - agent_selection
        And must set up the environment so that render(), step(), and observe()
        can be called without issues.
        Here it sets up the state dictionary which is used by step() and the 
        observations dictionary which is used by step() and observe()
        """
        # Reset parts of the PettingZoo env
        self.agents = self.possible_agents[:]
        self.rewards = {a: 0 for a in self.agents}
        self._cumulative_rewards = {a: 0 for a in self.agents}
        self.terminations = {a: False for a in self.agents}
        self.truncations = {a: False for a in self.agents}
        self.infos = {a: {} for a in self.agents}
        self.action_counts = {a: 0 for a in self.agents}
        self.agent_selection = self.agents[0]

        # Reset game objects
        self.round = 1
        self.turn = 1
        self.game = Game(num_players=len(self.agents), player_names=self.agents)

        self.observations = {a: self.observe(a) for a in self.agents}

        # Make a log output folder
        if self.log:
            self.log_dir = os.path.join(".", "logs", datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"))
            os.makedirs(self.log_dir)

        return self.observations, self.infos

    #===================================================================================================================
    def step(self, actions):
        """
        step(action) takes in an action for the current agent (specified by
        agent_selection) and needs to update
        - rewards
        - _cumulative_rewards (accumulating the rewards)
        - terminations
        - truncations
        - infos
        - agent_selection (to the next agent)
        And any internal state used by observe() or render()
        """
        print(actions)
        action = actions[self.agent_selection]

        if "Gain Food" in action.keys():
            # Determine die taken and food gained
            i = action["Gain Food"]
            if i == 0: food_gained = "Fish"
            elif i == 1: food_gained = "Rodent"
            elif i == 2: food_gained = "Fruit"
            elif i in [3,5]: food_gained = "Invertebrate"
            elif i in [4,6]: food_gained = "Seed"
            die_taken = "Invertebrate+Seed" if i in [5,6] else food_gained
            print(f"Taking {die_taken} and gaining {food_gained}.")
            # Take from birdfeeder
            self.game.birdfeeder.take(die_taken)
            self.game.players[self.agent_selection].editFood({food_gained: 1})
        else:
            raise NotImplementedError

        # Re-roll birdfeeder if it's empty
        if len(self.game.birdfeeder.food) == 0:
            print("Re-rolling birdfeeder because it's empty.")
            self.game.birdfeeder.roll()
        
        # Update observations
        self.observations = {a: self.observe(a) for a in self.agents}

    #===================================================================================================================
    def render(self):
        """
        Renders the environment. In human mode, it can print to terminal, open
        up a graphical window, or open up some other display that a human can 
        see and understand.
        """
        if self.render_mode == "ansi":
            # Print to terminal
            print(self.game)
        elif self.render_mode == "human":
            # Create the html file and save
            html = createHTML(round=self.round, turn=self.turn, eorgMat=self.game.end_of_round_goals, 
                              player=[i for i in range(len(self.game.player_names)) 
                                      if self.game.player_names[i]==self.agent_selection][0], 
                              birdfeeder=self.game.birdfeeder, birddeck=self.game.deck)
            with open(os.path.join(self.log_dir, f"Round_{self.round}_Turn_{self.turn}_Agent{self.agent_selection}_Action_{self.action_counts[self.agent_selection]}.html"), "w'") as f:
                f.write(html)

    #===================================================================================================================
    def save_snapshot(self):
        with open(os.path.join(self.log_dir, f"Round_{self.round}_Turn_{self.turn}_Agent{self.agent_selection}_Action_{self.action_counts[self.agent_selection]}.pkl"), "wb") as f:
            pickle.dump(self, f)