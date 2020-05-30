from QMap import QMap
import random

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
    
    def exploreGoal(self):
        trajectory = []
        cur_state = self.getStart()

        while cur_state not in self.end_states:
            valid_directions = self.qmap.getValidMoves(cur_state)
            cur_state = self.qmap.move(state_action)
