import pdb
import numpy as np
import matplotlib.pyplot as plt

#exp parameters
CHRO   = 16
DAY    = "D4"
REP    = 1

#get tad predictions from real Hi-C data
real_contact_data_STR = "HiC_Tool_Tads/tad_real_ipsc_day_"+str(DAY)+"_rep_"+str(REP)+"_chro_"+str(CHRO)+"_DI.txt"
real_TAD = np.loadtxt(real_contact_data_STR)

#get Tad predictions from structure
miss   = [2,4,6,8]
colors = ['blue', 'red', 'orange','yellow']
tads = {}
for mis in miss:
	loadstr        = "HiC_Tool_Tads/ipsc_"+str(mis)+"_"+str(REP)+"_1000_0.6_0.0001_400_50000_21_"+str(CHRO)+"_DI.txt"
	#loadstr        = "HiC_Tool_Tads/ipsc_"+str(mis)+"_"+str(REP)+"_1000_0_DI.txt"
	tads[mis]      = np.loadtxt(loadstr)
	
#Buidl actualy plot
fig, ax = plt.subplots(5)
TIME    = 0
level   = 4
ax[level].plot(np.clip(real_TAD, -10000,10000 ), color='black', label="hic")
ax[level].spines['top'].set_visible(False)
ax[level].spines['right'].set_visible(False)
#plot 4d prediciton
for m, mis in enumerate(miss):
	level -= 1
	curr_tad = tads[mis]
	ax[level].plot(np.clip(curr_tad,-1000,1000), color=colors[m], label=str(mis))
	ax[level].set_xticks([])
	ax[level].spines['top'].set_visible(False)
	ax[level].spines['right'].set_visible(False)
plt.savefig("Figures/Compare_DI/"+str(CHRO)+"_day_"+str(DAY)+'_rep_'+str(REP)+".png")



