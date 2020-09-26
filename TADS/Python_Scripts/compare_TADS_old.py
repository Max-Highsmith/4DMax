import pdb
import numpy as np
import matplotlib.pyplot as plt

##
#
# Show the 
##
#

#exp parameters
CHRO   = 16
DAY    = "D4"
REP    = 1


#get tad predictions from real Hi-C data
real_contact_data_STR = "HiC_Tool_Tads/tad_real_ipsc_day_"+str(DAY)+"_rep_"+str(REP)+"_chro_"+str(CHRO)+".npy"
real_TAD = np.load(real_contact_data_STR)


#get Tad predictions from structure
miss   = [2,4,6,8]
colors = ['blue', 'red', 'orange','yellow']
tads = {}

for mis in miss:
	temp      = np.load("HiC_Tool_Tads/ipsc_"+str(mis)+"_"+str(REP)+"_1000_0.6_0.0001_400_50000_21_"+str(CHRO)+".npy", allow_pickle=True, encoding='bytes')
	tads[mis] = temp.item()
	

#Buidl actualy plot
SCALE    = 100000
fig, ax = plt.subplots(1)
TIME    = 8
level   = 1
#plot real
for interval in range(0, real_TAD.shape[0]):
	ax.plot(real_TAD[interval]/SCALE, [level,level], color='black')
	ax.scatter(real_TAD[interval][0]/SCALE, [level], marker=9, color='black')
	ax.scatter(real_TAD[interval][1]/SCALE, [level], marker=8, color='black')

#plot 4d prediciton
for m, mis in enumerate(miss):
	level += 1
	curr_tad = tads[mis][TIME]
	for interval in range(0, curr_tad.shape[0]):
		ax.plot(curr_tad[interval]/SCALE, [level, level], color=colors[m])
		ax.scatter(curr_tad[interval][0]/SCALE, [level], marker=9, color=colors[m])
		ax.scatter(curr_tad[interval][1]/SCALE, [level], marker=8, color=colors[m])

ax.set_xlabel("loci (100kb)")
ax.set_yticks([1,2,3,4,5])
ax.set_yticklabels(['True Contact', 'D2', 'D4', 'D6', 'D8', 'D10'])
plt.show()



