class Grid:
    def __init__(self,rows,cols,win,lose):
        self.qValues = {}
        self.rows = rows
        self.cols = cols

        self.directions = ['up','down','left','right']
        
        for d in directions:
            self.qValues[d] = []
            for i in range(rows):
                self.qValues[d].append([])
                for j in range(cols):
                    self.qValues[d][i].append(0.0)
        
    def move(self,i,j,direction):
        x,y = i,j
        if direction == 'up':
            i = i - 1
        elif direction == 'down':
            i = i + 1
        elif direction == 'left':
            j = j - 1
        else:
            j = j + 1

        if (0<i<self.rows) and (0 < j < self.cols) :
            return i,j,self.maxQ(i,j)
        return x,y,None
    
    def maxQ(self,i,j):
        values = [self.qValues['up'][i][j],self.qValues['down'][i][j],self.qValues['left'][i][j],self.qValues['right'][i][j]]
        max_value = max(values)
        direction = self.directions[values.index(max_value)]
        return direction,max_value


