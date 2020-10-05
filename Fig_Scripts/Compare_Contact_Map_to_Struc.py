from scipy.stats import spearmanr
from Utils import util as ut
import numpy as np
import matplotlib.pyplot as plt
import pdb


##ARGS
chro  = 2
eta   = 1000
alpha = 0.6
lr    = 0.0001
res   = 50000
step  = 21
rep   = 1
epoch = 400

chros = list(range(15,19))#[19]
for chro in chros:
	mis = 2
	time =4

	reps = [1,2]

	mat_contacts   = {}
	mat_mis_struc  = {}
	mat_full_struc = {}

	fig, ax = plt.subplots(ncols=3, nrows=2)
	fig.suptitle(str(chro))
	for r, rep in enumerate(reps):
		FULL_STRUC_STRING   = "Generated_Structures/ipsc_full_rep_"+str(rep)+"_eta_"+str(eta)+"_alpha_"+str(alpha)+"_lr_"+str(lr)+"_epoch_"+str(epoch)+"_res_"+str(res)+"_step_"+str(step)+"_chro_"+str(chro)+".npy"
		MIS_STRUC_STRING   = "Generated_Structures/ipsc_missing_"+str(mis)+"_rep_"+str(rep)+"_eta_"+str(eta)+"_alpha_"+str(alpha)+"_lr_"+str(lr)+"_epoch_"+str(epoch)+"_res_"+str(res)+"_step_"+str(step)+"_chro_"+str(chro)+".npy"
		CONTACT_STRING = "Real_Data/iPluripotent/day_D2_rep_"+str(rep)+"_chro_"+str(chro)
		
		mat_contacts[r]      = ut.loadConstraintAsMat(CONTACT_STRING)
		mat_mis_struc[r]     = ut.loadStrucAtTimeAsMat(MIS_STRUC_STRING, time)
		mat_full_struc[r]    = ut.loadStrucAtTimeAsMat(FULL_STRUC_STRING,time)

	for r, rep in enumerate(reps):
		ax[r,0].set_ylabel("Rep "+str(rep))
		ax[r,0].imshow(np.clip(mat_contacts[r],0,30), cmap="Reds")
		ax[r,1].imshow(np.clip(mat_mis_struc[r], 0,10), cmap="Reds")
		ax[r,2].imshow(np.clip(mat_full_struc[r], 0,10), cmap="Reds")
		ax[r,0].set_xticks([])
		ax[r,0].set_yticks([])
		ax[r,1].set_xticks([])
		ax[r,1].set_yticks([])
		ax[r,2].set_xticks([])
		ax[r,2].set_yticks([])


	ax[0,0].set_xlabel("Real (SPC="+"{:.2f}".format(spearmanr(mat_contacts[0], mat_contacts[0], axis=None)[0])+")")
	ax[0,1].set_xlabel("Interp (SPC="+"{:.2f}".format(spearmanr(mat_contacts[0], mat_mis_struc[0], axis=None)[0])+")")
	ax[0,2].set_xlabel("Recon (SPC="+"{:.2f}".format(spearmanr(mat_contacts[0], mat_full_struc[0], axis=None)[0])+")")
	ax[1,0].set_xlabel("Real (SPC="+"{:.2f}".format(spearmanr(mat_contacts[0], mat_contacts[1], axis=None)[0])+")")
	ax[1,1].set_xlabel("Interp (SPC="+"{:.2f}".format(spearmanr(mat_contacts[1], mat_mis_struc[1], axis=None)[0])+")")
	ax[1,2].set_xlabel("Recon (SPC="+"{:.2f}".format(spearmanr(mat_contacts[1], mat_full_struc[1], axis=None)[0])+")")

	print(spearmanr(mat_contacts[0], mat_contacts[0], axis=None))
	print(spearmanr(mat_contacts[0], mat_full_struc[0], axis=None))
	print(spearmanr(mat_contacts[0], mat_mis_struc[0], axis=None))
	print(spearmanr(mat_contacts[0], mat_contacts[1], axis=None))
	print(spearmanr(mat_contacts[1], mat_full_struc[1], axis=None))
	print(spearmanr(mat_contacts[1], mat_mis_struc[1], axis=None))
	print(spearmanr(mat_contacts[0], mat_full_struc[0], axis=None))
	print(spearmanr(mat_contacts[0], mat_mis_struc[0], axis=None))
	print(spearmanr(mat_contacts[0], mat_contacts[1], axis=None))
	print(spearmanr(mat_contacts[1], mat_full_struc[1], axis=None))
	print(spearmanr(mat_contacts[1], mat_mis_struc[1], axis=None))
	
	plt.savefig("Figures/iPSC/Recon_Maps/vis_chro_"+str(chro)+"_time_"+str(time))
