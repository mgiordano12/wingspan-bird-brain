from pettingzoo import AECEnv
import functools
from copy import copy
from Game import Game
from Gameplay_Constants import NUMBER_OF_TURNS

class WingspanEnvironment(AECEnv):
    """ 
    The metadata holds environment constants. 
    """
    metadata = {
        "name": "WingspanEnvironment",
        "render_modes": ["human",],
    }

    def __init__(self, render_mode):
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
        self.reset()

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
        self.agents = copy(self.possible_agents)
        self.rewards = {a: 0 for a in self.agents}
        self._cumulative_rewards = {a: 0 for a in self.agents}
        self.terminations = {a: False for a in self.agents}
        self.terminations = {a: False for a in self.agents}
        self.infos = {a: {} for a in self.agents}
        self.agent_selection = self.agents[0]

        self.round = 1
        self.turns_lefts = NUMBER_OF_TURNS
        self.game = Game(num_players=len(self.agents), player_names=self.agents)

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

    def render(self):
        """
        Renders the environment. In human mode, it can print to terminal, open
        up a graphical window, or open up some other display that a human can 
        see and understand.
        """
        raise NotImplementedError

    # lru_cache allows observation and action spaces to be memoized, reducing clock cycles required to get each agent's space.
    # If your spaces change over time, remove this line (disable caching).
    # @functools.lru_cache(maxsize=None)
    def observation_space(self, agent):
        raise NotImplementedError
        return self.observation_spaces[agent]

    # If your spaces change over time, remove this line (disable caching).
    # @functools.lru_cache(maxsize=None)
    def action_space(self, agent):
        raise NotImplementedError
        return self.action_spaces[agent]