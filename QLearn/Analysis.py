from QMap import QMap
from QAgent import QAgent

class Analysis:
    def __init__(self,rows,cols,block,reward,start,end,gammaType='static'):
        self.rows = rows
        self.cols = cols
        self.block = block
        self.reward = reward
        self.start_states = start
        self.end_states = end
        #setting qMap
        self.qmap = QMap(rows,cols,gammaType)
        self.qmap.setQmap(block,reward)

        #setup QAgent
        self.agent = QAgent(self.qmap,self.start_states,self.end_states)

        self.directionMatrix = [['' for i in range(cols)] for j in range(rows)]

    def episode(self,exp_rate):
        trajectory = self.agent.exploreTrajectory(exp_rate)
        return trajectory
    
    def getDirectMatrix(self):
        matrix = []
        for i in range(self.rows):
            tmp = []
            for j in range(self.cols):
                tmp.append(self.qmap.maxQdirection((i,j)))
            matrix.append(tmp)
        for i in self.block:
            matrix[i[0]][i[1]] = '-'
        return matrix


    def trainConst(self,exp_rate,lr,gamma):
        num_ep = 0
        directMat = self.getDirectMatrix()
        length = 0
        trajectory2 = []
        print(directMat)
        while True:
            trajectory = self.episode(exp_rate)
            #change it
            self.qmap.updateQgrid(trajectory,lr)            
            print('-----------------------------------------------------')
            self.directionMatrix = [[j for j in i] for i in directMat]
            directMat = self.getDirectMatrix()
            length = length + len(trajectory)
            print(self.directionMatrix)
            num_ep = num_ep + 1
            exp_rate = exp_rate*0.98
            if (directMat != self.directionMatrix and num_ep > 5) or trajectory2 == trajectory:
                break
            trajectory2 = trajectory
        return num_ep,directMat,length
    
    def trainAdaptive(self,exp_rate,lr,gamma=1.0):
        num_ep = 0
        avg_trj = 0.0
        directMat = self.getDirectMatrix()
        length = 0
        gms = [gamma]
        trajectory2 = []
        while True:
            trajectory = self.episode(exp_rate)
            if len(trajectory) > avg_trj:
                gamma = gamma *0.9
                gms.append(gamma)
            elif len(trajectory) < avg_trj:
                gamma = gamma *1.1
                if gamma > 1:
                    gamma = 1.0
                gms.append(gamma)
            # update q grid
            self.qmap.updateQgrid(trajectory,lr,gamma)
            avg_trj = (avg_trj*num_ep + len(trajectory))/(num_ep+1)
            self.directionMatrix = [[j for j in i] for i in directMat]
            directMat = self.getDirectMatrix()
            length = length + len(trajectory)
            num_ep = num_ep + 1
            exp_rate = exp_rate*0.98
            if (directMat != self.directionMatrix and num_ep > 10 ) or trajectory2 == trajectory:
                break
            trajectory2 = trajectory
        return num_ep,directMat,length,gms

    def trainAdaptive2(self,exp_rate,lr,gamma=1.0):
        num_ep = 0
        avg_trj = 0.0
        directMat = self.getDirectMatrix()
        length = 0
        gms = [gamma]
        trajectory2 = []
        while True:
            trajectory = self.episode(exp_rate)
            if len(trajectory) > avg_trj:
                gamma = gamma *0.9
                gms.append(gamma)
                self.qmap.updateGamma(gamma)
            elif len(trajectory) < avg_trj:
                gamma = gamma *1.1
                if gamma > 1:
                    gamma = 1.0
                gms.append(gamma)
                self.qmap.updateGamma(gamma)
            # update q grid
            self.qmap.updateQgrid(trajectory,lr)
            avg_trj = (avg_trj*num_ep + len(trajectory))/(num_ep+1)
            self.directionMatrix = [[j for j in i] for i in directMat]
            directMat = self.getDirectMatrix()
            length = length + len(trajectory)
            num_ep = num_ep + 1
            exp_rate = exp_rate*0.96
            if (directMat != self.directionMatrix and num_ep > 10 ) or trajectory2 == trajectory:
                break
            trajectory2 = trajectory
        return num_ep,directMat,length,gms

    def trainAlgo2(self,exp_rate,lr):
        num_ep = 0
        directMat = self.getDirectMatrix()
        length = 0
        reward = 0.0
        while True:
            trajectoryL,trajectoryR = self.agent.doEpisode(exp_rate,lr)
            self.directionMatrix = [[j for j in i] for i in directMat]
            directMat = self.getDirectMatrix()
            length = length + trajectoryL
            reward = reward + trajectoryR
            num_ep = num_ep + 1
            exp_rate = exp_rate*0.95
            print(num_ep,' :> ',self.directionMatrix)
            print(num_ep,' >> ',directMat)
            print()
            if ( num_ep > 1 ) and (directMat == self.directionMatrix):
                print('----------FINALE MATRIX----------\n',self.directionMatrix)
                break

        return num_ep,directMat,length,self.qmap.gamma,reward