from Analysis import Analysis
import matplotlib.pyplot as plt

rows = 3
cols = 10
block = [(1,1),(1,3),(1,5),(1,6)]
reward = [ ((0,9),2.0), ((1,9),-2.0) ]
start_states = [(2,0)]
end_states = [ (0,9),(1,9) ]

constAnalysis = Analysis(rows,cols,block,reward,start_states,end_states)
adaptiveAnalysis = Analysis(rows,cols,block,reward,start_states,end_states)

episodesConst,matConst,constLength = constAnalysis.trainConst(1.0,0.5,0.5)
episodesAdap,matAdap,adapLength,gammas = adaptiveAnalysis.trainAdaptive(1.0,0.5,0.5)


print('Static Gamma')
print('episodes : ',episodesConst)
print('Total Trajectory Length : ',constLength)
print('Adaptive Gamma')
print('episodes : ',episodesAdap)
print('Total Trajectory Length : ',adapLength)
print('Num of Gamma change: ',len(gammas))
print('Gammas : ',gammas)
print('========================================================================')
episodes = [episodesConst,episodesAdap]
lengths = [constLength,adapLength]












x = [0,1]
#episodesConst = episodesConst*25
#episodesAdap = int(0.857*episodesConst)

fig, (ax1, ax2) = plt.subplots(1, 2)
fig.suptitle('Episodes and changing Gamma')
ax2.plot(x, episodes)
ax1.bar(x,lengths)
ax1.set_ylabel('Total Trajectory Length')
ax1.set_xticks(x,('Constant Gamma','Adaptive Gamma'))
plt.show()