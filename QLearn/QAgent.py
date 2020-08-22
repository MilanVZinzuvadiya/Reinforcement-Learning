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
    
    #chooseAction functio+n choose current state valid action from ['up','down','left','right']
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
        cur_state = self.getStart()
        trajectory = []
        tot_reward = 0.0
        while cur_state not in self.end_states:
            valid_directions = self.qmap.getValidMoves(cur_state)
            
            action = self.chooseAction(cur_state,valid_directions,exp_rate)
            state_action = cur_state[0],cur_state[1],action
            cur_state = self.qmap.move(state_action)
            cur_reward = self.qmap.rewards.getReward(cur_state)
            trajectory.append((state_action,cur_reward))
            tot_reward = tot_reward + cur_reward
        return trajectory,tot_reward
    
    def doEpisode(self,exp_rate,lr,adaptiveness):
        up_gamma = 1.0 + (adaptiveness/100.0)
        down_gamma = 1.0 - (adaptiveness/100.0)
        tr_length= 0
        cur_state = self.getStart()
        cur_reward = self.qmap.rewards.getReward(cur_state)
        cr_state = cur_state
        cr_reward = 0
        
        trajectory = []
        tot_reward = cur_reward
        while cur_state not in self.end_states:
            valid_directions = self.qmap.getValidMoves(cur_state)
            
            action = self.chooseAction(cur_state,valid_directions,exp_rate)
            state_action = cur_state[0],cur_state[1],action
            #self.qmap.updateQvalue(state_action,lr)

            
            
            reward_cur = cur_reward + self.qmap.qgrid.getQvalue(state_action)*self.qmap.gamma.getGamma(cur_state[0],cur_state[1])
            
            
            cur_state = self.qmap.move(state_action)
            cur_reward = self.qmap.rewards.getReward(cur_state)
            trajectory.append((state_action,cur_reward))
            tot_reward = cur_reward + tot_reward
            #reward_cur = self.qmap.rewards.getReward(cur_state) + self.qmap.qgrid.getQvalue(state_action)*self.qmap.gamma.getGamma(cur_state[0],cur_state[1])
            if reward_cur > cr_reward:
                self.qmap.gamma.setGamma(self.qmap.gamma.getGamma(cr_state[0],cr_state[1])*up_gamma,cr_state[0],cr_state[1])
            elif reward_cur < cr_reward:
                self.qmap.gamma.setGamma(self.qmap.gamma.getGamma(cr_state[0],cr_state[1])*down_gamma,cr_state[0],cr_state[1])

            tr_length += 1
            cr_reward = reward_cur
            cr_state = cur_state
            
        self.qmap.updateQgrid(trajectory,lr)
        self.qmap.rewards.resetRewards()
        
        return tr_length,tot_reward
