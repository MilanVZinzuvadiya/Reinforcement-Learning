class Reward:
    def __init__(self,rows,cols):
        self.cols = cols
        self.rows = rows
        self.rewards = {}
    
    def setReward(self,state,val):
        i = state
        assert i[0] < self.rows and i[1] < self.cols,"Invalid row and Col"
        if val == 0.0:
            self.rewards.pop(i,0.0)
        else:
            self.rewards[i] = val
    
    def getReward(self,state):
        if state not in self.rewards:
            return 0.0
        return self.rewards[state]

    def getRewards(self):
        return self.rewards
    
    def __eq__(self,r2):
        if self.cols == r2.cols and self.rows == r2.cols and self.rewards == r2.rewards:
            return True
        return False