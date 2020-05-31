from Reward import Reward
from Block import Block
from Qgrid import QGrid

class QMap:
    def __init__(self,rows,cols):
        self.rows = rows
        self.cols = cols
        self.blocks = Block(rows,cols)
        self.rewards = Reward(rows,cols)
        self.qgrid = QGrid(rows,cols)

    # block is list of wall in grid
    #       with state tuple as (i,j)
    # reward is list of pair [state,reward_value]
    def setQmap(self,block,reward):
        for b in block:
            self.blocks.doBlock(b)
        
        for r in reward:
            self.rewards.setReward(r[0],r[1])
    
    def updateQgrid(self,trajectory,lr,gamma):
        for state_action in reversed(trajectory):
            self.updateQvalue(state_action,lr,gamma)
    
    def updateQvalue(self,state_action,lr,gamma):
        cur_val = self.qgrid.getQvalue(state_action)
        cur_state = state_action[0],state_action[1]

        next_state = self.move(state_action)
        _,next_maxQ = self.qgrid.maxQ(next_state)

        reward = self.rewards.getReward(cur_state)

        new_val = cur_val + lr * (reward + gamma * next_maxQ - cur_val)
        self.qgrid.setQvalue(state_action,new_val)
    
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

        if (0<i<self.rows) and (0 < j < self.cols):
            return i,j
        return x,y
    
    def getValidMoves(self,state):
        directions = ['up','down','left','right']
        moves = [(-1,0),(1,0),(0,-1),(0,1)]
        blcks = self.blocks.getsBlocks()
        
        validDirections = []
        for i in range(4):
            x,y = state[0]+moves[i][0],state[1]+moves[i][1]
            if (x < self.rows ) and ( y< self.cols):
                if (x,y) not in blcks:
                    validDirections.append(directions[i])
        return validDirections

                    
                 

