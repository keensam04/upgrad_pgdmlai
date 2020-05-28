import numpy as np
import random
from itertools import groupby
from itertools import product



class TicTacToe():

    def __init__(self):
        """initialise the board"""
        
        # initialise state as an array
        self.state = [np.nan for _ in range(9)]  # initialises the board position, can initialise to an array or matrix
        # all possible numbers
        self.all_possible_numbers = [i for i in range(1, len(self.state) + 1)] # , can initialise to an array or matrix

        self.reset()


    def is_winning(self, curr_state):
        """Takes state as an input and returns whether any row, column or diagonal has winning sum
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan]
        Output = False"""
        winning_sum = 15
        if ((curr_state[0] + curr_state[1] + curr_state[2]) == winning_sum) or \
           ((curr_state[3] + curr_state[4] + curr_state[5]) == winning_sum) or \
           ((curr_state[6] + curr_state[7] + curr_state[8]) == winning_sum) or \
           ((curr_state[0] + curr_state[3] + curr_state[6]) == winning_sum) or \
           ((curr_state[1] + curr_state[4] + curr_state[7]) == winning_sum) or \
           ((curr_state[2] + curr_state[5] + curr_state[8]) == winning_sum) or \
           ((curr_state[0] + curr_state[4] + curr_state[8]) == winning_sum) or \
           ((curr_state[2] + curr_state[4] + curr_state[6]) == winning_sum):
            return True
        else:
            return False
 

    def is_terminal(self, curr_state):
        # Terminal state could be winning state or when the board is filled up

        if self.is_winning(curr_state) == True:
            return True, 'Win'

        elif len(self.allowed_positions(curr_state)) ==0:
            return True, 'Tie'

        else:
            return False, 'Resume'


    def allowed_positions(self, curr_state):
        """Takes state as an input and returns all indexes that are blank"""
        return [i for i, val in enumerate(curr_state) if np.isnan(val)]


    def allowed_values(self, curr_state):
        """Takes the current state as input and returns all possible (unused) values that can be placed on the board"""

        used_values = [val for val in curr_state if not np.isnan(val)]
        agent_values = [val for val in self.all_possible_numbers if val not in used_values and val % 2 !=0]
        env_values = [val for val in self.all_possible_numbers if val not in used_values and val % 2 ==0]

        return (agent_values, env_values)


    def action_space(self, curr_state):
        """Takes the current state as input and returns all possible actions, i.e, all combinations of allowed positions and allowed values"""
        allowed_values = self.allowed_values(curr_state)
        agent_actions = product(self.allowed_positions(curr_state), allowed_values[0])
        env_actions = product(self.allowed_positions(curr_state), allowed_values[1])
        return (agent_actions, env_actions)


    def state_transition(self, curr_state, curr_action):
        """Takes current state and action and returns the board position just after agent's move.
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan], action- [7, 9] or [position, value]
        Output = [1, 2, 3, 4, nan, nan, nan, 9, nan]
        """
        res_state = curr_state
        res_state[curr_action[0]] = curr_action[1]
        return res_state


    def reward(self, status):
        if status == 'Win':
            return 10
        elif status == 'Tie':
            return 0
        elif status == 'Resume':
            return -1
        else:
            return -10


    def step(self, curr_state, curr_action):
        """Takes current state and action and returns the next state, reward and whether the state is terminal. Hint: First, check the board position after
        agent's move, whether the game is won/loss/tied. Then incorporate environment's move and again check the board status.
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan], action- [7, 9] or [position, value]
        Output = ([1, 2, 3, 4, nan, nan, nan, 9, nan], -1, False)"""

        # validate agent action
        agent_actions, env_actions = self.action_space(curr_state)
        assert len([action for action in agent_actions if action == curr_action]) >= 1, 'invalid action'

        # apply agent's action and evaluate reward
        res_state = [state for state in curr_state]
        res_state = self.state_transition(res_state, curr_action)
        is_terminated, status = self.is_terminal(res_state)
        reward = self.reward(status)

        # apply environment's action if game is not terminated and re-evaluate reward
        if is_terminated == False:
            agent_actions, env_actions = self.action_space(res_state)
            env_action = random.choice([action for action in env_actions])
            res_state = self.state_transition(res_state, env_action)
            is_terminated, status = self.is_terminal(res_state)
            if (is_terminated == True) and (status == 'Win'):
                reward = self.reward('Loss')

        return (res_state, reward, is_terminated)


    def reset(self):
        return self.state
