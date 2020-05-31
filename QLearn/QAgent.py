from QMap import QMap
import random
import numpy as np

class QAgent:
    def __init__(self,qmap,rewards,end_states,start=None,start_list=None):
        self.qmap = qmap
        if start == start_list == None:
            raise "not valid start"
        self.start = start
        self.start_list = start_list
        self.end_states = end_states
        
    
    def getStart(self):
        if self.start != None:
            return self.start
        return self.start_list[random.randint(0,len(self.start_list)-1)]
    
    #chooseAction function choose current state valid action from ['up','down','left','right']
    def chooseAction(self,state,valid_actions,exp_rate):
        action = ''

        if np.random.uniform(0,1) <= exp_rate:
            action = np.random.choice(valid_actions)
        else:
            action = self.qmap.maxQdirection(state)
        
        if action not in valid_actions:
            action = np.random.choice(valid_actions)

        return action




    #perform one episode and return trajectory
    def exploreGoal(self,exp_rate):
        trajectory = []
        cur_state = self.getStart()

        while cur_state not in self.end_states:
            valid_directions = self.qmap.getValidMoves(cur_state)
            action = self.chooseAction(cur_state,valid_directions,exp_rate)
            state_action = cur_state[0],cur_state[1],action
            trajectory.append(state_action)
            cur_state = self.qmap.move(state_action)
        
        return trajectory
