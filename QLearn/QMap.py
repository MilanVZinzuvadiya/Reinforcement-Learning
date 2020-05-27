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
    
    def setQmap(self,block,reward):
        for b in block:
            self.blocks.doBlock(b)
        
        for r in reward:
            self.rewards.setReward(r[0],r[1])
    
    def updateQgrid(self,trajectory):
        for state in reversed(trajectory):
            pass