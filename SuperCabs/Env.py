# Import routines
import numpy as np
import random

# Defining constants
m = 5 # number of cities, ranges from 1 ... m
t = 24 # number of hours, ranges from 0 ... t-1
d = 7  # number of days, ranges from 0 ... d-1
C = 5 # Per hour fuel and other costs
R = 9 # per hour revenue from a passenger

MAX_REQUESTS = 15
EPISODE_LENGTH_IN_HOURS = t*30 #30 days

lambda_loc_0=2
lambda_loc_1=12
lambda_loc_2=4
lambda_loc_3=7
lambda_loc_4=8

Time_matrix = np.load("TM.npy")

class CabDriver():

    def __init__(self, debug=False):
        """define action space and state space and initialize state and tracking info"""
        self.debug = debug

        self.action_space = [(i,j) for i in range(1,m+1) for j in range(1,m+1) if i!=j]+[(0,0)]
        self.state_space = [(i,j,k) for i in range(1,m+1) for j in range(0,t) for k in range(0,d)]
        self.state_size = m + t + d

        self.reset()

        if self.debug:
            print('CabDriver initialized with following config', {
                'action_space': self.action_space,
                'state_space_length': len(self.state_space),
                'state_size': self.state_size,
                'total_reward': self.total_reward,
                'total_time_consumed': self.total_time_consumed,
                'total_time_steps': self.total_time_steps,
                'state_init': self.state_init
                })


    ## Encoding state (or state-action) for NN input
    def encode_state_v1(self, state):
        """convert the state into a vector so that it can be fed to the NN. This method converts a given state into a vector format. The vector is of size m + t + d."""
        location_array = np.zeros(m)
        hour_of_day_array = np.zeros(t)
        day_of_week_array = np.zeros(d)

        location_array[state[0]-1] = 1
        hour_of_day_array[state[1]] = 1
        day_of_week_array[state[2]] = 1

        encoded_state = np.concatenate((location_array, hour_of_day_array, day_of_week_array), axis=None)

        if self.debug:
            print('encode_state_v1: ', state, ' -> ', encoded_state)

        return encoded_state

    ## Encoding state (or state-action) for NN input
    def encode_state_v2(self, state):
        """convert the state into a vector so that it can be fed to the NN. This method converts a given state into a vector format. The vector is of size m * t * d."""
        encoded_state = np.zeros(len(self.state_space))
        encoded_state[self.state_space.index(state)] = 1

        if self.debug:
            print('encode_state_v2: ', state, ' -> ', encoded_state)

        return encoded_state


    def get_poisson(self, location):
        if location == 1:
            requests = np.random.poisson(lambda_loc_0)
        if location == 2:
            requests = np.random.poisson(lambda_loc_1) 
        if location == 3:
            requests = np.random.poisson(lambda_loc_2) 
        if location == 4:
            requests = np.random.poisson(lambda_loc_3) 
        if location == 5:
            requests = np.random.poisson(lambda_loc_4)

        return requests


    ## Getting number of requests
    def requests(self, state):
        """Determining the number of requests basis the location. 
        Use the table specified in the MDP and complete for rest of the locations"""
        
        location = state[0]
        requests = self.get_poisson(location)
        while requests == 0:
            requests = self.get_poisson(location)

        if requests > MAX_REQUESTS:
            requests = MAX_REQUESTS

        possible_actions_index = random.sample(range(0, (m-1)*m), requests)
        possible_actions_index.append((m-1)*m)
        random.shuffle(possible_actions_index)

        actions = [self.action_space[i] for i in possible_actions_index]

        if self.debug:
            print('possible actions: ', state, ' -> ', actions)

        return actions   

    def step(self, state, action, Time_matrix=Time_matrix):
        start_loc = state[0]
        hour_of_day = state[1]
        day_of_week = state[2]
        
        pickup_loc = action[0]
        drop_loc = action[1]
        
        time_spent_for_pickup = int(Time_matrix[start_loc-1][pickup_loc-1][hour_of_day][day_of_week])
        pickup_hour = hour_of_day + time_spent_for_pickup
        pickup_day = day_of_week
        
        if pickup_hour >= 24 :
          pickup_hour=pickup_hour - 24
          pickup_day = pickup_day + 1
          if pickup_day >= 7:
            pickup_day = pickup_day - 7

        time_spent_for_ride = int(Time_matrix[pickup_loc-1][drop_loc-1][pickup_hour][pickup_day])

        if action==(0,0):
            reward = -1*C
            next_loc = start_loc
            next_hour_of_day = hour_of_day + 1  
            next_day_of_week = day_of_week
        else:
            reward = (R * time_spent_for_ride) - (C * (time_spent_for_pickup + time_spent_for_ride))
            next_loc = drop_loc
            if pickup_hour == hour_of_day & time_spent_for_ride == 0:
                next_hour_of_day = hour_of_day + 1
            else:
                next_hour_of_day = pickup_hour + time_spent_for_ride
            next_day_of_week = day_of_week

        if next_hour_of_day >= 24 :
           next_hour_of_day = next_hour_of_day - 24
           next_day_of_week = next_day_of_week + 1
           if next_day_of_week >= 7:
               next_day_of_week = next_day_of_week - 7
     
        next_state = (next_loc, next_hour_of_day, next_day_of_week)

        self.total_reward = self.total_reward + reward
        self.total_time_steps = self.total_time_steps + 1
        if (time_spent_for_pickup + time_spent_for_ride) > 0:
            self.total_time_consumed = self.total_time_consumed + time_spent_for_pickup + time_spent_for_ride
        else:
            self.total_time_consumed = self.total_time_consumed + 1

        is_terminal = False
        if self.total_time_consumed >= EPISODE_LENGTH_IN_HOURS:
            is_terminal = True

        if self.debug:
            print('step: ', {
                'state':state,
                'action':action,
                'time_spent_for_pickup':time_spent_for_pickup,
                'pickup_hour':pickup_hour,
                'pickup_day':pickup_day,
                'time_spent_for_ride':time_spent_for_ride
            })

        return next_state, reward, is_terminal
    
    def tracking_info(self):
        return self.total_reward, self.total_time_consumed, self.total_time_steps

    def reset(self):
        self.loc_space=np.random.choice(np.arange(1,m+1)) 
        self.hour_of_day=np.random.choice(np.arange(0,t)) 
        self.day_of_week=np.random.choice(np.arange(0,d)) 
        self.total_reward=0
        self.total_time_consumed=0
        self.total_time_steps = 0
      
        self.state_init = (self.loc_space,self.hour_of_day,self.day_of_week)

        return self.state_init
