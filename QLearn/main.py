from Analysis import Analysis
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from matplotlib.ticker import MaxNLocator
import csv
import os
for adaptiveness in range(1,50):
    for experiment_no in range(100):
        '''
        Gridworld Parameters
        '''
        rows = 1
        cols =10
        block = []
        reward = [ ((0,1),1.0),( (0,5),2.0 ),((0,9),2.0) ]
        possible_reward = 5.0
        start_states = [(0,0)]
        end_states = [ (0,9) ]
        '''
        GAMMA
        '''
        #adaptiveness = 25


        constAnalysis = Analysis(rows,cols,block,reward,start_states,end_states)
        algo2analysis = Analysis(rows,cols,block,reward,start_states,end_states,'dynamic')

        episodesConst,matConst,constLength,reward_const = constAnalysis.trainConst(1.0,0.5,0.5)
        episodesALgo2,matAlgo2,algo2Len,gamma,reward = algo2analysis.trainAlgo2(1.0,0.5,adaptiveness)

        #print('Static Gamma')
        #print('episodes : ',episodesConst)
        #print('Total Trajectory Length : ',constLength)
        #print('Total reward : ',reward_const)
        constEfficency = reward_const/constLength
        #print('Efficency per state : ',constEfficency)
        '''print('Adaptive Gamma')
        print('episodes : ',episodesAdap)
        print('Total Trajectory Length : ',adapLength)
        print('Num of Gamma change: ',len(gammas))
        print('Gammas : ',gammas)
        '''
        #print('=================================================')


        #print('Algo2 gamma')
        #print('episodes : ',episodesALgo2)
        #print('Total Trajectory Length : ',algo2Len)
        #print('Total reward : ',reward)
        algo2efficiency = reward/algo2Len
        #print('Efficiency per state : ',algo2efficiency)
        gms = gamma.getGammas()
        #print(gms)


        episodes = [episodesConst,episodesALgo2]
        lengths = [constLength,algo2Len]
        eficiency = [constEfficency,algo2efficiency]
        returns = [reward_const,reward]

        winner =  'Const' if (constEfficency > algo2efficiency) else  'Adap';
        #make list according to data file : AdaptiveGamma.csv
        experimentData = [[rows,cols,adaptiveness,possible_reward,episodesConst,constLength,reward_const,episodesALgo2,algo2Len,reward,winner]]

        file = open('data/AdaptiveGamma.csv','a+',newline='')
        with file:
            write = csv.writer(file)
            write.writerows(experimentData)

        '''
        Graph ploting and saving
        '''
        plTitle = 'Adaptive Gamma Comparision for {} row x {} col Gridworld with {} percent adaptiveness : exp {}'.format(rows,cols,adaptiveness,experiment_no)
        img_tit = str(rows)+'x'+str(cols)+' '+str(adaptiveness)+' adap exp'+str(experiment_no)

        x = [0,1]
        #episodesConst = episodesConst*25
        #episodesAdap = int(0.857*episodesConst)

        fig = plt.figure(figsize=(13,9),dpi=120)
        fig.tight_layout(pad=2.0)
        spec = gridspec.GridSpec(ncols=2, nrows=3, figure=fig)

        fig.suptitle(plTitle)

        ax1 = fig.add_subplot(spec[0,0])
        ax1.bar(x,lengths)
        ax1.set_title('Total \nvisited states')
        ax1.set_xticks(np.arange(2))
        ax1.set_xticklabels(['Const','Adapt'])


        ax2 = fig.add_subplot(spec[2,0])
        ax2.set_title('Total Episodes')
        ax2.bar(x, episodes)
        ax2.set_xticks(np.arange(2))
        ax2.set_xticklabels(['Const','Adapt'])
        rects = ax2.patches
        ax2.yaxis.set_major_locator(MaxNLocator(integer=True))
        for rect,label in zip(rects,episodes):
            height = rect.get_height()
            ax2.text(rect.get_x() + rect.get_width() / 2, height, label,
                    ha='center', va='bottom')


        ax3 = fig.add_subplot(spec[2,1])
        ax3.set_title('Efficiency in Training')
        ax3.bar(x,eficiency)
        ax3.set_xticks(np.arange(2))
        ax3.set_xticklabels(['Const','Adapt'])
        ax3.set_xlabel('Average reward per visiting state in training\n $**_{efficiency = TotalReturn/ TotalVisitedStaes }$')


        ax4 = fig.add_subplot(spec[0,1])
        ax4.set_title('Total Returns')
        ax4.bar(x,returns)
        ax4.set_xticks(np.arange(2))
        ax4.set_xticklabels(['Const','Adapt'])

        import itertools
        gm1 = list(itertools.chain.from_iterable(gms))


        ax5 = fig.add_subplot(spec[1,:])

        ax5.set_title('Gamma of all states after training')
        ax5.plot(gm1)
        fig_save_dir = 'data/'+str(rows)+'x'+str(cols)+'/'+str(adaptiveness)+' adaptiveness/' 
        if not os.path.exists(fig_save_dir):
            os.makedirs(fig_save_dir)
        plt.savefig(fig_save_dir+img_tit+'.png')
        plt.clf()
        print('Adap :',adaptiveness,'experiment :',experiment_no)
