class QGrid:
    def __init__(self,rows,cols):
        self.qValues = {}
        self.rows = rows
        self.cols = cols
        self.directions = ['up','down','left','right']

        for d in self.directions:
            self.qValues[d] = []
            for i in range(rows):
                self.qValues[d].append([])
                for j in range(cols):
                    self.qValues[d][i].append(0.0)
    
    
    
    def maxQ(self,state):
        i,j = state[0],state[1]
        values = [self.qValues['up'][i][j],self.qValues['down'][i][j],self.qValues['left'][i][j],self.qValues['right'][i][j]]
        max_value = max(values)
        direction = self.directions[values.index(max_value)]
        return direction,max_value

    #getQvalue return value of Q(s,a)
    # it takes state_action tuple as
    #               state_action[0] = i (row)
    #               state_action[1] = j (col)
    #               state_action[2] = direction ('up','down','left','right')
    def getQvalue(self,state_action):
        if state_action[0]< self.rows and state_action[1] < self.cols:
            return 0.0
        return self.qValues[state_action[2]][state_action[0]][state_action[1]]

    #state_action = (row,col,direction)
    def setQvalue(self,state_action,val):
        i,j,direction = state_action[0],state_action[1],state_action[2]
        self.qValues[direction][i][j] = val

    def setQvalueMatrix(self,qvalues):
        self.rows = len(qvalues['up']) 
        self.cols = len(qvalues['up'][self.rows-1])
        self.qValues = qvalues
    
    def getQvalueMatrix(self,direction):
        return self.qValues[direction]
    
    def __eq__(self,grid2):
        return self.qValues == grid2.qValues