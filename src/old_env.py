# 
# https://pettingzoo.farama.org/content/environment_creation/

import functools
from Gameplay_Constants import NUMBER_OF_TURNS, BIRDFEEDER_FACES, NUMBER_BIRD_CARDS, MAX_NUMBER_DIE_IN_BIRDFEEDER
import gymnasium
from gymnasium.wrappers import FlattenObservation
import numpy as np
from gymnasium.spaces import Box, Dict, Discrete, MultiBinary, MultiDiscrete

from pettingzoo import AECEnv
from pettingzoo.utils import agent_selector, wrappers

from Game import Game

### We are going to stick with one agent for now
NUM_AGENTS = 1

def create_env(render_mode=None):
    """
    The env function often wraps the environment in wrappers by default.
    You can find full documentation for these methods
    elsewhere in the developer documentation.
    """
    internal_render_mode = render_mode if render_mode != "ansi" else "human"
    env = raw_env(render_mode=internal_render_mode)
    print(env.test)
    # This wrapper is only for environments which print results to the terminal
    if render_mode == "ansi":
        env = wrappers.CaptureStdoutWrapper(env)
    print(env.test)
    # this wrapper helps error handling for discrete action spaces
    env = wrappers.AssertOutOfBoundsWrapper(env)
    print(env.test)
    # Provides a wide vareity of helpful user errors
    # Strongly recommended
    env = wrappers.OrderEnforcingWrapper(env)
    print(env.test)
    return env


class raw_env(AECEnv):
    """
    The metadata holds environment constants. From gymnasium, we inherit the "render_modes",
    metadata which specifies which modes can be put into the render() method.
    At least human mode should be supported.
    The "name" metadata allows the environment to be pretty printed.
    """

    metadata = {"render_modes": ["human"], "name": "rps_v2"}

    def __init__(self, render_mode=None):
        """
        The init method takes in environment arguments and
         should define the following attributes:
        - possible_agents
        - render_mode
        """
        self.possible_agents = ["player_" + str(r) for r in range(NUM_AGENTS)]
        # optional: a mapping between agent name and ID
        self.agent_name_mapping = dict(
            zip(self.possible_agents, list(range(len(self.possible_agents))))
        )

        self.render_mode = render_mode

        self.test = 'hello?'

    # Observation space should be defined here.
    # lru_cache allows observation and action spaces to be memoized, reducing clock cycles required to get each agent's space.
    # If your spaces change over time, remove this line (disable caching).
    @functools.lru_cache(maxsize=None)
    def observation_space(self, agent):
        # gymnasium spaces are defined and documented here: https://gymnasium.farama.org/api/spaces/
        # TODO: Will need to flatten this when using.  See https://gymnasium.farama.org/api/wrappers/observation_wrappers/#gymnasium.wrappers.FlattenObservation
        obs_space = gymnasium.spaces.Dict(
            {
                "Bird Position" : MultiDiscrete([20,]*NUMBER_BIRD_CARDS), # 0-14 gamemat, 15 agent hand, 16 tray, 17 agent discarded, 18 unknown, 19 tucked
                # ^^ TODO ^^: add more channels to bird position observation if we want to include other player's boards and hands
                # "Goals" : MultiDiscrete([NUMBER_END_ROUND_GOALS,]*4),
                "Birdfeeder" : MultiDiscrete([BIRDFEEDER_FACES+1,]*MAX_NUMBER_DIE_IN_BIRDFEEDER), # +1 for die out of feeder
                # "Food in Hand" : Box(low=0, high=2**63-2, shape=(NUMBER_FOOD_TYPES,), dtype=int),
                # "Round Number" : Box(low=1, high=NUMBER_OF_ROUNDS, dtype=int), # Default shape of 1
                # "Turns Left" : Box(low=0, high=np.max(NUMBER_OF_TURNS), dtype=int), # Default shape of 1
                # "Bonus in Hand": MultiDiscrete([3,]*NUMBER_BONUS_CARDS), # 0 agent hand, 1 agent discarded, 2 unknown
                # "Cached Food": Box(low=0, high=2**63-2, shape=[NUMBER_HABITATS, NUMBER_CARDS_PER_HABITAT, 1], dtype=int), # number cached food in each spot on the gamemate
                # ^^ TODO ^^: increase size of last dim to include all other players later
                # TODO "Tucked cards" - add later if we care about where the card is tucked or how many cards the other players have tucked, Box(low=0, high=NUM_CARDS, shape=[NUM_HABITATS, NUM_CARDS_PER_HABITAT, 1], dtype=int), increase last dim later if we want to include tucked card counts for other players
                # NOTE, TO THINK ABOUT: do we want to directly represent birdcard attributes here - e.g., nest types, wingspans, food cost for birds???
            }
        )
        return obs_space

    # Action space should be defined here.
    # If your spaces change over time, remove this line (disable caching).
    @functools.lru_cache(maxsize=None)
    def action_space(self, agent):
        # gymnasium spaces are defined and documented here: https://gymnasium.farama.org/api/spaces/
        # TODO: Will need to flatten this when using.  See https://gymnasium.farama.org/api/wrappers/observation_wrappers/#gymnasium.wrappers.FlattenObservation
        # TODO: Need to update for starting decisions
        action_space = gymnasium.spaces.Dict(
            {
                # "Play Bird" : MultiDiscrete(np.ones([NUMBER_HABITATS, NUMBER_BIRD_CARDS])),
                "Gain Food" : Discrete(len(BIRDFEEDER_FACES)),  # Gain food one at a time
                # ^^ TODO ^^: Think about this one. Keep as 1 action in dict or break into 5 actions in dict, 1 for each food type
                # "Lay Egg" : MultiDiscrete(np.ones([NUMBER_HABITATS, NUMBER_CARDS_PER_HABITAT])), # One egg at a time
                "Gain Bird" : Discrete(NUMBER_BIRD_CARDS + 1), # One card at a time, mask those not available, +1 is choose random
                # "Powers" : Discrete(NUMBER_UNIQUE_POWERS + 1),  # This is whether or not to "do" the action, and all other options should be masked at this step
                # "Board Trade": Discrete(4), # 3 for doing the trades on the board, 1 for "NO"
                # "Discard Food" : Discrete(NUMBER_FOOD_TYPES + (((NUMBER_FOOD_TYPES-1)**2)*NUMBER_FOOD_TYPES)), # Area in () represents ability to trade
                #                             # Two of any food for one of another. There are (NUMBER_FOOD_TYPES-1)**2 combos of two food (that aren't the food I need) 
                #                             # to trade for the food I need.  Multiply by NUMBER_FOOD_TYPES (food I need)
                # "Discard Egg" : MultiDiscrete(np.ones([NUMBER_HABITATS, NUMBER_CARDS_PER_HABITAT])),
                # "Discard or Tuck Bird From Hand" : Discrete(NUMBER_BIRD_CARDS), # Can encapsulate these in one since they are functionally equivilant to us (which card disappears)
                # "Bonus Card" : Discrete(NUMBER_BONUS_CARDS),
                # "Cache or Keep Food" : Discrete(2), # Cache or Keep
                # # ^^ TODO ^^: Think about this one. Include keep food in Gain Food above and make cache separate? Break into separate actions for each food type?
                # "Repeat Power" : Discrete(NUMBER_UNIQUE_POWERS), # Which power to repeat
                # "Move Bird" : Discrete(NUMBER_HABITATS), # TODO: Use masking to disable the habitat the bird is already in
                # "Reroll Birdfeeder": Discrete(2),
            }
        )
        return action_space

    def render(self):
        """
        Renders the environment. In human mode, it can print to terminal, open
        up a graphical window, or open up some other display that a human can see and understand.
        """
        ### TODO: @Owen- connect up with your GUI.  Right now I have it just printing things
        print(self.game)


    def close(self):
        """
        Close should release any graphical displays, subprocesses, network connections
        or any other environment data which should not be kept around after the
        user is no longer using the environment.
        """
        ### TODO: @Owen
        pass

    # NOTE: I think we just call 
    def observe(self, agent):
        """
        Observe should return the observation of the specified agent. This function
        should return a sane observation (though not necessarily the most up to date possible)
        at any time after reset() is called.
        """
        # observation of one agent is the previous state of the other
        return np.array(self.observations[agent])

    # NOTE: To get started, I think we should simply provide rewards as when points are realized (eggs laid, card played, end of round goal, Bonus card realized or lost)
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
        Here it sets up the state dictionary which is used by step() and the observations dictionary which is used by step() and observe()
        """

        # I think we want to point this at our initialized players?
        self.agents = self.possible_agents[:]

        # TODO
        self.rewards = {agent: 0 for agent in self.agents}
        self._cumulative_rewards = {agent: 0 for agent in self.agents}

        # I think termination is supposed to represent a player having no more turns.  Can we use this for end of rounds?
        self.terminations = {agent: False for agent in self.agents}
        # TODO: What is truncation supposed to represent
        self.truncations = {agent: False for agent in self.agents}

        # TODO: Not sure what these are used for
        self.infos = {agent: {} for agent in self.agents}
        self.state = {agent: None for agent in self.agents}
        self.observations = {agent: None for agent in self.agents}

        """
        Our agent_selector utility allows easy cyclic stepping through the agents list.
        """
        self.agent_selection = self.possible_agents[0]
        # NOTE: I'm not sure we'll be able to use this since sometimes order changes :(
        # self._agent_selector = agent_selector(self.agents)
        # self.agent_selection = self._agent_selector.next()

        self.round_number = 1
        self.turns_left = NUMBER_OF_TURNS
        self.game = Game(num_players=len(self.possible_agents), player_names=self.possible_agents)
        # TODO: For multiple players, randomize order

    # NOTE: I think this is the are that is going to interact with the bulk of our code
    def step(self, action):
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
        if (
            self.terminations[self.agent_selection]
            or self.truncations[self.agent_selection]
        ):
            # handles stepping an agent which is already dead
            # accepts a None action for the one agent, and moves the agent_selection to
            # the next dead agent,  or if there are no more dead agents, to the next live agent
            self._was_dead_step(action)
            return

        # TODO: This is the mechanism they use to move turns.  Need to update fro wingspan
        # agent = self.agent_selection

        # the agent which stepped last had its _cumulative_rewards accounted for
        # (because it was returned by last()), so the _cumulative_rewards for this
        # agent should start again at 0
        # self._cumulative_rewards[agent] = 0

        # stores action of current agent
        self.state[self.agent_selection] = action

        ## TODO: Blocking out any reards for now until we get gameplay up and running
        # collect reward if it is the last agent to act
        # if self._agent_selector.is_last():
        #     # rewards for all agents are placed in the .rewards dictionary
        #     self.rewards[self.agents[0]], self.rewards[self.agents[1]] = REWARD_MAP[
        #         (self.state[self.agents[0]], self.state[self.agents[1]])
        #     ]

        #     self.num_moves += 1
        #     # The truncations dictionary must be updated for all players.
        #     self.truncations = {
        #         agent: self.num_moves >= NUM_ITERS for agent in self.agents
        #     }

        #     # observe the current state
        #     for i in self.agents:
        #         self.observations[i] = self.state[
        #             self.agents[1 - self.agent_name_mapping[i]]
        #         ]
        # else:
        #     # necessary so that observe() returns a reasonable observation at all times.
        #     self.state[self.agents[1 - self.agent_name_mapping[agent]]] = NONE
        #     # no rewards are allocated until both players give an action
        #     self._clear_rewards()

        # selects the next agent.
        # TODO: We are going to have to make out own "agent selector" which determines the next steps
        # self.agent_selection = self._agent_selector.next()
    
        # Adds .rewards to ._cumulative_rewards
        # self._accumulate_rewards()

        if self.render_mode == "human":
            self.render()
