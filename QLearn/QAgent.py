from QMap import QMap
import random
import numpy as np

class QAgent:
    def __init__(self,qmap,start,end):
        self.qmap = qmap
        self.start = start
        self.end_states = end
        
    
    def getStart(self):
        return self.start[random.randint(0,len(self.start)-1)]
    
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
    def exploreTrajectory(self,exp_rate):
        trajectory = []
        cur_state = self.getStart()
        print(self.end_states)
        while cur_state not in self.end_states:
            valid_directions = self.qmap.getValidMoves(cur_state)
            
            action = self.chooseAction(cur_state,valid_directions,exp_rate)
            state_action = cur_state[0],cur_state[1],action
            trajectory.append(state_action)
            cur_state = self.qmap.move(state_action)
            print(state_action,cur_state)
        
        return trajectory
