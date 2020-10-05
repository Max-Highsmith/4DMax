import pdb
from scipy.stats import pearsonr
from scipy.stats import spearmanr
import numpy as np
import matplotlib.pyplot as plt
from Utils import util as ut
fig, ax = plt.subplots(6,6)
for day, time in zip([0,1,2,3,4,5], [0,4,8,12,16,20]):
	real1  = 1/ut.loadConstraintAsMat("Synthetic_Data/Synthetic_Contact_Maps/struc1_"+str(day)+".txt", res=100000)
	real2  = 1/ut.loadConstraintAsMat("Synthetic_Data/Synthetic_Contact_Maps/struc2_"+str(day)+".txt", res=100000)
	full1  = 1/ut.loadStrucAtTimeAsMat("Generated_Structures/synthetic_full_rep_1_eta_10_alpha_1.0_lr_0.01_epoch_1000_res_100000_step_21_chro_all.npy", time)
	full2  = 1/ut.loadStrucAtTimeAsMat("Generated_Structures/synthetic_full_rep_2_eta_10_alpha_1.0_lr_0.01_epoch_1000_res_100000_step_21_chro_all.npy", time)
	if day == 0 or day ==5:
		struc1  = 1/ut.loadStrucAtTimeAsMat("Generated_Structures/synthetic_full_rep_1_eta_10_alpha_1.0_lr_0.01_epoch_1000_res_100000_step_21_chro_all.npy", time)
		struc2  = 1/ut.loadStrucAtTimeAsMat("Generated_Structures/synthetic_full_rep_2_eta_10_alpha_1.0_lr_0.01_epoch_1000_res_100000_step_21_chro_all.npy", time)
	else:
		struc1 = 1/ut.loadStrucAtTimeAsMat("Generated_Structures/synthetic_missing_"+str(day)+"_rep_1_eta_10_alpha_1.0_lr_0.01_epoch_1000_res_100000_step_21_chro_all.npy", time)
		struc2 = 1/ut.loadStrucAtTimeAsMat("Generated_Structures/synthetic_missing_"+str(day)+"_rep_2_eta_10_alpha_1.0_lr_0.01_epoch_1000_res_100000_step_21_chro_all.npy", time)
	print("DAY:"+str(day))
	#print("spearman r1,s1:"+str(spearmanr(real1, struc1, axis=None)))
	#print("spearman r2,s2:"+str(spearmanr(real2, struc2, axis=None)))
	#print("spearman r1,s2:"+str(spearmanr(real1, struc2, axis=None)))
	#print("spearman r2,s1:"+str(spearmanr(real2, struc1, axis=None)))
	#print("spearman r1,f1:"+str(spearmanr(real1, full1, axis=None)))
	#print("spearman r2,f2:"+str(spearmanr(real2, full2, axis=None)))
	print("\n")
	print("pearson r1,s1:"+"{:.2f}".format(pearsonr(real1.flatten(), struc1.flatten())[0]))
	print("pearson r2,s2:"+"{:.2f}".format(pearsonr(real2.flatten(), struc2.flatten())[0]))
	#print("pearson r1,s2:"+str(pearsonr(real1.flatten(), struc2.flatten())))
	#print("pearson r2,s1:"+str(pearsonr(real2.flatten(), struc1.flatten())))
	print("pearson r1,f1:"+"{:.2f}".format(pearsonr(real1.flatten(), full1.flatten())[0]))
	print("pearson r2,f2:"+"{:.2f}".format(pearsonr(real2.flatten(), full2.flatten())[0]))
	print("\n")
	print("\n")

	one = ax[0,day].imshow(real1, cmap="Reds", vmin=0, vmax=5)
	two = ax[1,day].imshow(real2, cmap="Reds", vmin=0, vmax=5)
	fig.colorbar(one, ax=ax[0,day])
	fig.colorbar(two, ax=ax[1,day])
	ax[0,day].set_xticks([])
	ax[1,day].set_xticks([])
	ax[0,day].set_yticks([])
	ax[1,day].set_yticks([])

	one = ax[2,day].imshow(full1, cmap="Reds", vmin=0, vmax=5)
	two = ax[3,day].imshow(full2, cmap="Reds", vmin=0, vmax=5)
	fig.colorbar(one, ax=ax[2,day])
	fig.colorbar(two, ax=ax[3,day])
	ax[2,day].set_xticks([])
	ax[3,day].set_xticks([])
	ax[2,day].set_yticks([])
	ax[3,day].set_yticks([])

	one = ax[4,day].imshow(struc1, cmap="Reds", vmin=0, vmax=5)
	two = ax[5,day].imshow(struc2, cmap="Reds", vmin=0, vmax=5)
	fig.colorbar(one, ax=ax[4,day])
	fig.colorbar(two, ax=ax[5,day])
	ax[4,day].set_xticks([])
	ax[5,day].set_xticks([])
	ax[4,day].set_yticks([])
	ax[5,day].set_yticks([])



ax[5,0].set_xlabel("Day 0")
ax[5,1].set_xlabel("Day 1")
ax[5,2].set_xlabel("Day 2")
ax[5,3].set_xlabel("Day 3")
ax[5,4].set_xlabel("Day 4")
ax[5,5].set_xlabel("Day 5")
ax[0,0].set_ylabel("Real 1")
ax[1,0].set_ylabel("Real 2")
ax[2,0].set_ylabel("Recon 1")
ax[3,0].set_ylabel("Recon 2")
ax[4,0].set_ylabel("Interp 1")
ax[5,0].set_ylabel("Interp 2")
plt.savefig("Figures/Synthetic/comps.png")
plt.show()
