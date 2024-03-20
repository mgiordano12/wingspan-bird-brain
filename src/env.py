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
from gymnasium.spaces import Discrete, MultiDiscrete, Box
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
        self.possible_agents = ["bird-brain",]
        self.render_mode = render_mode
        self.log = log
        self.reset()

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
        self.agents = copy(self.possible_agents)
        self.rewards = {a: 0 for a in self.agents}
        self._cumulative_rewards = {a: 0 for a in self.agents}
        self.terminations = {a: False for a in self.agents}
        self.truncations = {a: False for a in self.agents}
        self.infos = {a: {} for a in self.agents}
        self.action_counts = {a: 0 for a in self.agents}
        self.agent_selection = self.agents[0]

        self.observation_spaces = {
            a: gymnasium.spaces.Dict({
                "observation": gymnasium.spaces.Dict({
                    "Birdfeeder" : MultiDiscrete([len(BIRDFEEDER_FACES)+1,]*MAX_NUMBER_DIE_IN_BIRDFEEDER), # +1 for die out of feeder
                }),
                "action_mask": gymnasium.spaces.Dict({
                    "Gain Food": Box(low=0, high=1, shape=(len(FOOD_TYPES),), dtype="int8")
                })
            })
            for a in self.agents
        }

        self.action_spaces = {
            a: gymnasium.spaces.Dict({
                "Gain Food" : Discrete(len(FOOD_TYPES)), # Gain food one at a time
            })
            for a in self.agents
        }

        # Reset game objects
        self.round = 1
        self.turn = 1
        self.game = Game(num_players=len(self.agents), player_names=self.agents)

        # Make a log output folder
        if self.log:
            self.log_dir = os.path.join(".", "logs", datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"))
            os.makedirs(self.log_dir)

        return self.observation_spaces, self.infos

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
        raise NotImplementedError

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

    def observe(self, agent):
        """
        Should return the observations in action mask for the agent
        """
        observation = {
            # 0=Fish, 1=Rodent, 2=Fruit, 3=Invertebrate, 4=Seed, 5=Invertebrate+seed, 6=dieOutOfFeeder
            "Birdfeeder": [
                np.argwhere(np.array(BIRDFEEDER_FACES)==self.game.birdfeeder.food[i])[0][0] if i < len(self.game.birdfeeder.food) else 6
                for i in range(MAX_NUMBER_DIE_IN_BIRDFEEDER)
            ]
        }

        action_mask = {
            "Gain Food": np.array([1 if f in str(self.game.birdfeeder.food) else 0 for f in FOOD_TYPES], dtype="int8")
        }

        return {"observation": observation, "action_mask": action_mask}

    #===================================================================================================================
    def save_snapshot(self):
        with open(os.path.join(self.log_dir, f"Round_{self.round}_Turn_{self.turn}_Agent{self.agent_selection}_Action_{self.action_counts[self.agent_selection]}.pkl"), "wb") as f:
            pickle.dump(self, f)


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