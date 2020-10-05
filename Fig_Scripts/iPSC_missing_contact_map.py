import cupy as cp
from scipy.stats import spearmanr
import pdb
from Utils import util as ut
import numpy as np
import matplotlib.pyplot as plt




missings        = [2,4,6,8]#,6,8]
reps            = [1,2]
times           = [0,4,8,12,16,20]
res             = 50000
spear           = np.zeros((len(times), len(missings), len(reps)))
for t, time in enumerate(times): #8,12,16,20]:
	for m, mis in enumerate(missings):
		for r, rep in enumerate(reps):
			struc = np.load("Generated_Structures/ipsc_missing_"+str(mis)+"_rep_"+str(rep)+"_eta_1000_alpha_0.6_lr_0.0001_epoch_400_res_50000_step_21_chro_15.npy")
			contact    = np.loadtxt("Real_Data/iPluripotent/day_D"+str(mis)+"_rep_"+str(rep)+"_chro_15")

			row     = (contact[:,0].astype(int)/res).astype(int)
			col     = (contact[:,1].astype(int)/res).astype(int)
			minn    = np.min((row,col))
			row     = row - minn
			col     = col - minn
			wish    = ut.getWishDistGPU(cp.asarray(struc[time]), cp.asarray(row), cp.asarray(col))
			hic     = contact[:,2]
			spear[t, m, r] = spearmanr(cp.asnumpy(hic), cp.asnumpy(wish), axis=None)[0]


##make graph for s
plt.close()
plt.clf()
plt.cla()
fig, ax = plt.subplots(1, figsize=(10,5))
for m, mis in enumerate(missings):
	for r, rep in enumerate(reps):
		print(m,r)
		labstring = "missing:"+str(mis)+" rep:"+str(rep)
		print(labstring)
		ax.plot((-1)*spear[:,m, r], label=labstring)

ax.legend()
ax.set_title("SPC with Contact Matrices")
ax.set_xticks([0,1,2,3,4,5])
ax.set_xticklabels(['0','2','4','6','8','10'])
ax.set_ylabel("SPC")
ax.set_xlabel("Missing Contact Map")
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.savefig("Figures/Contact_Struc_Comp/iPSC_missing.png")
