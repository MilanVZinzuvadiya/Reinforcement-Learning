from Analysis import Analysis


rows = 5
cols =10
block = [(0,1)]
reward = [ ((0,1),1.0),( (0,5),2.0 ),((3,5),2.0) ]
start_states = [(0,0)]
end_states = [ (3,5) ]

constAnalysis = Analysis(rows,cols,block,reward,start_states,end_states)
#adaptiveAnalysis = Analysis(rows,cols,block,reward,start_states,end_states)
algo2analysis = Analysis(rows,cols,block,reward,start_states,end_states,'dynamic')

episodesConst,matConst,constLength,reward_const = constAnalysis.trainConst(1.0,0.5,0.5)
#episodesAdap,matAdap,adapLength,gammas = adaptiveAnalysis.trainAdaptive2(1.0,0.5,0.5)
episodesALgo2,matAlgo2,algo2Len,gamma,reward = algo2analysis.trainAlgo2(1.0,0.5)

print('Static Gamma')
print('episodes : ',episodesConst)
print('Total Trajectory Length : ',constLength)
print('Total reward : ',reward_const)
constEfficency = reward_const/constLength
print('Efficency per state : ',constEfficency)
'''print('Adaptive Gamma')
print('episodes : ',episodesAdap)
print('Total Trajectory Length : ',adapLength)
print('Num of Gamma change: ',len(gammas))
print('Gammas : ',gammas)
'''
print('=================================================')


print('Algo2 gamma')
print('episodes : ',episodesALgo2)
print('Total Trajectory Length : ',algo2Len)
print('Total reward : ',reward)
algo2efficiency = reward/algo2Len
print('Efficiency per state : ',algo2efficiency)
gms = gamma.getGammas()
print(gms)


episodes = [episodesConst,episodesALgo2]
lengths = [constLength,algo2Len]
eficiency = [constEfficency,algo2efficiency]
returns = [reward_const,reward]





import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from matplotlib.ticker import MaxNLocator

x = [0,1]
#episodesConst = episodesConst*25
#episodesAdap = int(0.857*episodesConst)

fig = plt.figure()
fig.tight_layout(pad=2.0)
spec = gridspec.GridSpec(ncols=2, nrows=3, figure=fig)

fig.suptitle('Episodes and changing Gamma')

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

#anno_opts = dict(xy=(0.5, 0.5), xycoords='axes fraction',
#                 va='center', ha='center')
ax5 = fig.add_subplot(spec[1,:])
#ax5.annotate('changes in Gamma during Training', **anno_opts)
ax5.set_title('Gamma of all states after training')
ax5.plot(gm1)
plt.show()



#cm2 = list(itertools.chain.from_iterable(algo2analysis.agent.qmap.getQmap('right')))
#cm3 = list(itertools.chain.from_iterable(constAnalysis.agent.qmap.getQmap('right')))
#cm4 = list(itertools.chain.from_iterable(adaptiveAnalysis.agent.qmap.getQmap('right')))
