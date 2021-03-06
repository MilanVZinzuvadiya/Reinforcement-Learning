from Reward import Reward
from Block import Block
from QGrid import QGrid
from Gamma import Gamma


class QMap:
    Initial_gamma = 0.5
    def __init__(self,rows,cols,gammaType='static'):
        self.rows = rows
        self.cols = cols
        self.blocks = Block(rows,cols)
        self.rewards = Reward(rows,cols)
        self.qgrid = QGrid(rows,cols)
        self.gamma = Gamma(QMap.Initial_gamma,rows,cols,gammaType)

    # block is list of wall in grid
    #       with state tuple as (i,j)
    # reward is list of pair [state,reward_value]
    def setQmap(self,block,reward):
        for b in block:
            self.blocks.doBlock(b)
        
        for r in reward:
            self.rewards.setReward(r[0],r[1])
    
    def getQmap(self,direction):
        return self.qgrid.getQvalueMatrix(direction)

    def updateQgrid(self,trajectory,lr):
        for state_action_reward in reversed(trajectory):
            self.updateQvalue(state_action_reward,lr)
    
    def updateQvalue(self,state_action_reward,lr):
        cur_val = self.qgrid.getQvalue(state_action_reward[0])
        cur_state = state_action_reward[0][0],state_action_reward[0][1]

        next_state = self.move(state_action_reward[0])
        _,next_maxQ = self.qgrid.maxQ(next_state)

        reward = state_action_reward[1]
        new_val = cur_val + lr * (reward + self.gamma.getGamma(cur_state[0],cur_state[1]) * next_maxQ - cur_val)
        self.qgrid.setQvalue(state_action_reward[0  ],new_val)
    
    def updateGamma(self,ngamma,row=0,col=0):
        self.gamma.setGamma(ngamma,row,col)

    def maxQdirection(self,state):
        direction,max_value = self.qgrid.maxQ(state)
        return direction

    #move return value of row,col
    # it takes previous state_action tuple as
    #               state_action[0] = i (row)
    #               state_action[1] = j (col)
    #               state_action[2] = direction ('up','down','left','right')

    def move(self,p_state_action):
        x,y = p_state_action[0],p_state_action[1]
        i,j = x,y
        direction = p_state_action[2]
        if direction == 'up':
            i = i - 1
        elif direction == 'down':
            i = i + 1
        elif direction == 'left':
            j = j - 1
        else:
            j = j + 1
        
        if (0<= i <self.rows) and (0 <= j < self.cols):
            return i,j
        
        return x,y
    
    def getValidMoves(self,state):
        directions = ['up','down','left','right']
        moves = [(-1,0),(1,0),(0,-1),(0,1)]
        blcks = self.blocks.getsBlocks()
        
        validDirections = []
        for i in range(4):
            x,y = state[0]+moves[i][0],state[1]+moves[i][1]
            if (x < self.rows ) and ( y< self.cols) and x >= 0 and y >= 0 :
                if (x,y) not in blcks:
                    validDirections.append(directions[i])
        return validDirections


                    
                 

