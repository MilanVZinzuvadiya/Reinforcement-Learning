from Analysis import Analysis
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from matplotlib.ticker import MaxNLocator
import csv
import os
from matplotlib import colors
import matplotlib

######################################################################################
def annotate_heatmap(im, data=None, valfmt="{x:.2f}",
                     textcolors=("black", "white"),
                     threshold=None, **textkw):
    """
    A function to annotate a heatmap.

    Parameters
    ----------
    im
        The AxesImage to be labeled.
    data
        Data used to annotate.  If None, the image's data is used.  Optional.
    valfmt
        The format of the annotations inside the heatmap.  This should either
        use the string format method, e.g. "$ {x:.2f}", or be a
        `matplotlib.ticker.Formatter`.  Optional.
    textcolors
        A pair of colors.  The first is used for values below a threshold,
        the second for those above.  Optional.
    threshold
        Value in data units according to which the colors from textcolors are
        applied.  If None (the default) uses the middle of the colormap as
        separation.  Optional.
    **kwargs
        All other arguments are forwarded to each call to `text` used to create
        the text labels.
    """

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts
###########################################################################################

'''
BULK GRIDWORLD for experments
'''

#rows_list = [3,3,4,5,10,10]
#cols_list = [3,5,5,7,10,11]

rows_list = [10,10]
cols_list = [10,11]

block_list = [
#    [(1,1)],
#    [(1,1),(1,3)],
#    [(1,2)],
#    [(1,2),(1,3),(1,4),(2,1),(2,4),(3,0)],
    [],
    [(0,6),(1,1),(1,3),(1,6),(1,8),(2,4),(2,6),(3,0),(4,0),(4,1),(4,3),(4,6),(4,9),(5,0),(5,4),(5,8),(5,9),(6,9),(7,1),(7,4),(7,6),(8,7),(8,9),(9,3)]
]
reward_list = [
#    [ ((0,2),2.0), ((2,2),3.0) ],
#    [ ((2,1),2.0), ((0,3),2.0), ((2,4),3.0) ],
#    [ ((3,1),2.0), ((0,4),2.0), ((1,3),3.0) ],
#    [ ((0,2),2.0), ((1,1),2.0), ((2,5),2.0), ((2,6),2.0), ((3,1),2.0), ((2,0),3.0) ],
    [ ((9,0),2.0), ((9,1),2.0), ((9,3),2.0), ((8,0),2.0), ((9,9),3.0) ],
    [ ((1,9),2.0), ((4,4),2.0), ((4,5),2.0), ((4,7),2.0), ((6,5),2.0), ((7,7),2.0), ((8,2),2.0), ((8,6),2.0), ((9,8),2.0), ((9,0),3.0) ]
]
#possible_reward_list = [5,7,7,13,11,21]
possible_reward_list = [11,21]
start_states_list = [
#    [(0,0)],
#    [(0,0)],
#    [(0,0)],
#    [(2,3)],
    [(0,0)],
    [(2,0)]
]
end_states_list = [
#    [(2,2)],
#    [(2,4)],
#    [(1,3)],
#    [(2,0)],
    [(9,9)],
    [(9,0)]
]

'''
Gridworld Parameters
'''
'''
rows = 4
cols =5
block = [(1,1),(0,3)]
reward = [ ((0,2),2.0),( (2,2),3.0 ) ]
possible_reward = 5.0
start_states = [(0,0)]
end_states = [ (2,2) ]'''

ada = [1,3,5,10,15,20,25,30,35,40,45]
for (rows,cols,block,reward,possible_reward,start_states,end_states) in zip(rows_list,cols_list,block_list,reward_list,possible_reward_list,start_states_list,end_states_list):
    for adaptiveness in ada:
        for experiment_no in range(100):
            
            '''
            GAMMA
            '''
            #adaptiveness = 25


            constAnalysis = Analysis(rows,cols,block,reward,start_states,end_states)
            algo2analysis = Analysis(rows,cols,block,reward,start_states,end_states,'dynamic')

            episodesConst,matConst,constLength,reward_const = constAnalysis.trainConst(1.0,0.5,0.5)
            episodesALgo2,matAlgo2,algo2Len,gamma,reward_algo2 = algo2analysis.trainAlgo2(1.0,0.5,adaptiveness)

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
            algo2efficiency = reward_algo2/algo2Len
            #print('Efficiency per state : ',algo2efficiency)
            gms = gamma.getGammas()
            #print(gms)


            episodes = [episodesConst,episodesALgo2]
            lengths = [constLength,algo2Len]
            eficiency = [constEfficency,algo2efficiency]
            returns = [reward_const,reward_algo2]

            winner =  'Const' if (constEfficency > algo2efficiency) else  'Adap';
            #make list according to data file : AdaptiveGamma.csv
            experimentData = [[rows,cols,adaptiveness,possible_reward,episodesConst,constLength,reward_const,episodesALgo2,algo2Len,reward_algo2,winner]]

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

            fig = plt.figure(figsize=(14,10),dpi=120)
            fig.tight_layout(pad=3.0)
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

            '''
            ax5 = fig.add_subplot(spec[1,:])

            ax5.set_title('Gamma of all states after training')
            ax5.plot(gm1)
            ''' 
            

            #results of Gamma update
            ax5 = fig.add_subplot(spec[1,1])
            im = ax5.imshow(gms,cmap=plt.cm.Greens)
            #texts = annotate_heatmap(im)
            ax5.set_title('Statewise updated Gamma')
            ax5.set_xticks(np.arange(cols))
            ax5.set_yticks(np.arange(rows))
            plt.colorbar(im)
            
            # Gridworld

            
            norm = matplotlib.colors.BoundaryNorm(np.linspace(-50.0, 50, 8), 4)
            fmt = matplotlib.ticker.FuncFormatter(lambda x, pos: grid_labels[::-1][norm(x)])
            
            ax6 = fig.add_subplot(spec[1,0])
            grid = [[-100.0 for c in range(cols)] for r in range(rows)]
            for b in block:
                grid[b[0]][b[1]] = 100.0
            for s in start_states:
                grid[s[0]][s[1]] = 50.0
            for rwd in reward:
                tmp = rwd[0]
                grid[tmp[0]][tmp[1]] = -25.0
            for g in end_states:
                grid[g[0]][g[1]] = 0.0
            qrates = ['Block','Start','End','Reward','-']
            norm = matplotlib.colors.BoundaryNorm(np.linspace(-101.0, 101.0, 6), 5)
            fmt = matplotlib.ticker.FuncFormatter(lambda x, pos: qrates[::-1][norm(x)])
            im = ax6.imshow(grid,cmap=plt.cm.Blues)
            #annotate_heatmap(im, valfmt=fmt, size=9, fontweight="bold", threshold=-1,
            #       textcolors=("red", "black"))

            ax6.set_xticks(np.arange(cols))
            ax6.set_yticks(np.arange(rows))
            ax6.set_title('Gridworld')

            fig_save_dir = 'data/'+str(rows)+'x'+str(cols)+'/'+str(adaptiveness)+' adaptiveness/' 
            if not os.path.exists(fig_save_dir):
                os.makedirs(fig_save_dir)
            
            plt.savefig(fig_save_dir+img_tit+'.png')
            plt.clf()
            plt.close()
            print(rows,'x',cols,'Adap :',adaptiveness,'experiment :',experiment_no)
