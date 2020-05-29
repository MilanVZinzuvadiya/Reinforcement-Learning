from QGrid import QGrid
from Reward import Reward

r = Reward(3,3)
r2 = Reward(3,3)
print(r==r2)
r.setReward(1,1,5)
r.setReward(1,1,6)
r2.setReward(1,1,6)
r2.setReward(1,1,5)
print(r==r2)

print(r.getRewards())
print(r2.getRewards())