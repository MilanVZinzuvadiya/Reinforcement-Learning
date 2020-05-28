from QGrid import QGrid
from Reward import Reward
import random

class QAgent:
    def __init__(self,qgrid,rewards,start=None,start_list=None):
        self.qgrid = qgrid
        self.rewards = rewards
        self.start = start
        self.start_list = start_list
    
    def getStart(self):
        if self.start != None:
            return self.start
        return self.start_list[0]
