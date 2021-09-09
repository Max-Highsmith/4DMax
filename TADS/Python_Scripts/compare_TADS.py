import sys
sys.path.append(".")
import pdb
import numpy as np
import matplotlib.pyplot as plt
from Utils import tads as tt


#exp parameters
CHRO   = 1
REP    = 1
REPS   = [1,2]

#missing times
MISS   = [2,4,6,8]

#4D model to sample tads from
DAY    = "D4"
MISS_TIME  = 4
FULL_TIME  = 8

#time on 4d model to sample from
TIME       = 8
OTHER_TIME = 20
OTHER_DAY  = 'PSC'
	
real_TAD = {}
#get tad predictions from real Hi-C dataa
for rep in REPS:
	real_contact_data_STR = "HiC_Tool_Tads/tad_real_ipsc_day_"+str(DAY)+"_rep_"+str(rep)+"_chro_"+str(CHRO)+".npy"
	real_TAD[rep] = np.load(real_contact_data_STR)


#get Tad predictions from structure
colors = ['blue', 'red', 'orange','yellow']
tads = {}

for mis in MISS:
	temp      = np.load("HiC_Tool_Tads/ipsc_"+str(mis)+"_"+str(REP)+"_1000_0.6_0.0001_400_50000_21_"+str(CHRO)+".npy", allow_pickle=True, encoding='bytes')
	tads[mis] = temp.item()
	

fullTAD  = np.load("HiC_Tool_Tads/ipscFull_"+str(REP)+"_1000_0.6_0.0001_400_50000_21_"+str(CHRO)+".npy", allow_pickle=True, encoding='bytes')
fullTAD  = fullTAD.item()


#Buidl actualy plot
SCALE    = 1000000
fig, ax = plt.subplots(1)
level   = 0
rep_colors = ['black', 'blue']
#plot real
for r, rep in enumerate(REPS):
	level +=1
	for interval in range(0, real_TAD[rep].shape[0]):
		ax.plot(real_TAD[rep][interval]/SCALE, [level,level], color=rep_colors[r])
		ax.scatter(real_TAD[rep][interval][0]/SCALE, [level], marker=9, color=rep_colors[r])
		ax.scatter(real_TAD[rep][interval][1]/SCALE, [level], marker=8, color=rep_colors[r])

#plot 4d prediciton
level +=1
#curr_tad = tads[FULL_TIME][TIME]
curr_tad  = fullTAD[TIME]
for interval in range(0, curr_tad.shape[0]):
	ax.plot(curr_tad[interval]/SCALE, [level, level], color='green')
	ax.scatter(curr_tad[interval][0]/SCALE, [level], marker=9, color='green')
	ax.scatter(curr_tad[interval][1]/SCALE, [level], marker=8, color='green')

level +=1
curr_tad = tads[MISS_TIME][TIME]
#curr_tad  = fullTAD[TIME]
for interval in range(0, curr_tad.shape[0]):
	ax.plot(curr_tad[interval]/SCALE, [level, level], color='orange')
	ax.scatter(curr_tad[interval][0]/SCALE, [level], marker=9, color='orange')
	ax.scatter(curr_tad[interval][1]/SCALE, [level], marker=8, color='orange')

level +=1
curr_tad = tads[MISS_TIME][OTHER_TIME]
for interval in range(0, curr_tad.shape[0]):
	ax.plot(curr_tad[interval]/SCALE, [level, level], color='red')
	ax.scatter(curr_tad[interval][0]/SCALE, [level], marker=9, color='red')
	ax.scatter(curr_tad[interval][1]/SCALE, [level], marker=8, color='red')


#print("rep2:"+str(tt.getPercentOverlap(real_TAD[1], real_TAD[1])))
#print("rep2:"+str(tt.getPercentOverlap(real_TAD[1], real_TAD[2])))
print("rep2:"+str(tt.getPercentOverlap(real_TAD[2], real_TAD[1])))
print("recon:"+str(tt.getPercentOverlap(fullTAD[TIME], real_TAD[1])))
print("interp:"+str(tt.getPercentOverlap(tads[MISS_TIME][TIME], real_TAD[1])))
print("other:"+str(tt.getPercentOverlap(tads[MISS_TIME][OTHER_TIME], real_TAD[1])))
print("NEW")
print(np.mean(tt.getTadSetSim(real_TAD[2], real_TAD[1])))
print(np.mean(tt.getTadSetSim(real_TAD[1], real_TAD[2])))
print(np.mean(tt.getTadSetSim(real_TAD[1], tads[FULL_TIME][TIME])))
print(np.mean(tt.getTadSetSim(real_TAD[1], tads[MISS_TIME][TIME])))
print(np.mean(tt.getTadSetSim(real_TAD[1], tads[MISS_TIME][OTHER_TIME])))

ax.set_xlabel("loci (1mb)")
ax.set_yticks([1,2,3,4,5])
ax.set_yticklabels(['Hi-C rep1 ('+str(DAY)+')', 'Hi-C rep2 ('+str(DAY)+')', '4D reconstruction ('+str(DAY)+')', '4D interpolation ('+str(DAY)+')', '4D Different time ('+str(OTHER_DAY)+')'])
plt.title("Chro "+str(CHRO))
plt.show()



