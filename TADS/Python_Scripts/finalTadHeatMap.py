import pdb
import numpy as np
import matplotlib.pyplot as plt
from Utils import tads as tt

#exp parameters
CHROS  = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,'X']
REP    = 2
REPS   = [1,2]

#missing times
MISS   = [2,4,6,8]

#4D model to sample tads from
DAY    = "D4"

#time on 4d model to sample from
DAYS  = np.array(['B','D2','D4','D6','D8','ES'])


real_TAD = {}
#get tad predictions from real Hi-C dataa
for chro in CHROS:
	for day in DAYS:
		for rep in REPS:
			real_contact_data_STR = "HiC_Tool_Tads/tad_real_ipsc_day_"+str(day)+"_rep_"+str(rep)+"_chro_"+str(chro)+".npy"
			real_TAD[chro, rep, day] = np.load(real_contact_data_STR)


#get Tad predictions from structure
colors = ['blue', 'red', 'orange','yellow']
tads = {}

for rep in REPS:
	for chro in CHROS:
		for mis in MISS:
			temp      = np.load("HiC_Tool_Tads/ipsc_"+str(mis)+"_"+str(rep)+"_1000_0.6_0.0001_400_50000_21_"+str(chro)+".npy", allow_pickle=True, encoding='bytes')
			tads[chro, mis,rep] = temp.item()
		

#Fill Bar Information
bar = np.zeros((len(CHROS), 4, 5))
compfunc = tt.getPercentOverlap
#def compfunc(x,y):
#	return np.mean(tt.getTadSetSim(x,y)[0])

worse=0
same=0
better=0

for c, chro in enumerate(CHROS):
	for t, (day, indx, mis) in enumerate(zip(['D2', 'D4', 'D6','D8'], [4,8,12,16], MISS)):
		print(str(day),",",str(indx))
		base = real_TAD[chro, 1,day] #TADS identified from hic
		#bar[c, t, 0] = compfunc(real_TAD[chro, 1, day], base)
		bar[c,t, 0] = compfunc(real_TAD[chro, 2, day], base)
		leftIndx  = indx - 4
		rightIndx = indx + 4 
		leftDay   = DAYS[np.where(DAYS == day)[0] -1][0]
		rightDay  = DAYS[np.where(DAYS == day)[0] +1][0]
		leftMis   = mis - 2
		rightMis  = mis + 2
		if mis !=8:
			bar[c, t,1] = compfunc(tads[chro, rightMis,1][indx], base)
			bar[c, t,3] = compfunc(tads[chro, rightMis,1][indx], real_TAD[chro,2,day])
		else:
			bar[c, t,1] = compfunc(tads[chro, leftMis,1][indx], base)
			bar[c, t,3] = compfunc(tads[chro, leftMis,1][indx], real_TAD[chro,2,day])
		bar[c,t,2] = compfunc(tads[chro, mis,1][indx], base)
		#left and right neighbors
		bar[c,t,4]  = compfunc(tads[chro, mis,2][indx],real_TAD[chro,2,day])
		#bar[c,t,3]  = compfunc(real_TAD[chro,1,leftDay], base)
		#bar[c,t,4]  = compfunc(real_TAD[chro,1, rightDay], base)
		#bar[c,t,3] = compfunc(tads[chro, mis][leftIndx], base)
		#bar[c,t,4] = compfunc(tads[chro, mis][rightIndx], base)
		if ((bar[c,t,2] < bar[c,t,3]) and (bar[c,t,2] < bar[c,t,4])):
			worse = worse+1
		elif ((bar[c,t,2] > bar[c,t,3]) and (bar[c,t,2] > bar[c,t,4])):
			better = better+1
		else:
			same = same+1
tot = worse+same+better
print("worse:", str(worse), str(worse/tot))
print("same:", str(same), str(same/tot))
print("better:", str(better), str(better/tot))
		
#fig, ax = plt.subplots(len(CHROS))
#for c, chro in enumerate(CHROS):
fig, ax = plt.subplots(5,4)
for c, chro in enumerate(CHROS):
	ax[int(c%5), int(c/5)].imshow(bar[c], cmap="Greens", vmin=0, vmax=1)
	for (j, i), label in np.ndenumerate(bar[c]):
		#print("i",str(i))
		#print("j",str(j))
		#print("Axis:"+str(int(c/4))+":"+str(int(c%4)))
		#ax[c].text(i,j, "{0:0.2f}".format(bar[c,j,i]), ha='center', va='center', fontsize="xx-small", color="white")
		#ax[c].set_ylabel("Chro "+str(chro))
		#ax[c].set_yticklabels(["D2","D4","D6","D8"])
		#ax[c].set_yticks([0,1,2,3])
		#ax[c].set_xticks([])
		ax[int(c%5),int(c/5)].text(i,j, "{0:0.2f}".format(bar[c,j,i]), ha='center', va='center', fontsize="x-small", color="white")
		ax[int(c%5),int(c/5)].set_ylabel("Chro "+str(chro))
		ax[int(c%5),int(c/5)].set_yticklabels(["D2","D4","D6","D8"])
		ax[int(c%5),int(c/5)].set_yticks([0,1,2,3])
		ax[int(c%5),int(c/5)].set_xticks([])
ax[4,3].set_xticklabels(["HiC Rep", "4D Recon 1", "4D Interp 1", "4D Recon 2", "4D Recon 2"])
ax[4,3].set_xticks([0,1,2,3,4])
plt.xticks(rotation=90)


pdb.set_trace()
plt.show()



