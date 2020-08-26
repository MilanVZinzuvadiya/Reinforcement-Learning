class Gamma:
    def __init__(self,gamma,row=0,col=0,type='static'):
        self.gammas = {}
        self.gamma = gamma
        self.row = row
        self.col = col
        self.static = False
        if type == 'static':
            self.static=True
    
    def getGamma(self,row=0,col=0):
        if (row > self.row) or (col > self.col) or self.static:
            return self.gamma
        return self.gammas.setdefault((row,col),self.gamma)
    
    def setGamma(self,ngamma,row=0,col=0):
        if ngamma > 0.9 or ngamma < 0.1:
            return
        if row > self.row or col > self.col:
            return
        if self.static:
            self.gamma = ngamma
        else:
            self.gammas[(row,col)] = ngamma
    
    def getGammas(self):
        if self.static:
            return self.gamma
        
        gammas = []
        for i in range(self.row):
            r = []
            for j in range(self.col):
                r.append(self.getGamma(i,j))
            gammas.append(r)
        return gammas 

