import glob
from scipy.stats import spearmanr
from Utils import util as ut
import numpy as np
import matplotlib.pyplot as plt
import pdb


##ARGS
chro  = 19
eta   = 1000
alpha = 0.6
lr    = 0.0001
res   = 50000
step  = 21
rep   = 1
epoch = 400

mis = 2
time =2

reps = [1,2]

CHROS = list(range(1,23))
for chro in CHROS:
	mat_contacts   = {}
	mat_mis_struc  = {}
	mat_full_struc = {}

	fig, ax = plt.subplots(ncols=3, nrows=2)
	fig.suptitle("Chro "+str(chro))
	for r, rep in enumerate(reps):
		FULL_STRUC_STRING   = "Generated_Structures/cardio_full_rep_"+str(rep)+"_eta_1000_alpha_0.6_lr_0.0001_epoch_400_res_1_step_15_chro_"+str(chro)+".npy"
		MIS_STRUC_STRING    = "Generated_Structures/cardio_missing_2_rep_"+str(rep)+"_eta_1000_alpha_0.6_lr_0.0001_epoch_400_res_1_step_15_chro_"+str(chro)+".npy"
		CONTACT_STRING      = "Real_Data/Cardiomyocyte/RUES2/By_Chros/*_MES_Rep"+str(rep)+"_500KB_"+str(chro)
		CONTACT_STRING = glob.glob(CONTACT_STRING)[0]
		mat_contacts[r]      = ut.loadConstraintAsMat(CONTACT_STRING, res=1)
		mat_mis_struc[r]     = ut.loadStrucAtTimeAsMat(MIS_STRUC_STRING, time)
		mat_full_struc[r]    = ut.loadStrucAtTimeAsMat(FULL_STRUC_STRING,time)

	for r, rep in enumerate(reps):
		ax[r,0].set_ylabel("Rep "+str(rep))
		ax[r,0].imshow(np.clip(mat_contacts[r],0,30), cmap="Reds")
		ax[r,1].imshow(np.clip(mat_mis_struc[r], 0,10), cmap="Reds")
		ax[r,2].imshow(np.clip(mat_full_struc[r], 0,10), cmap="Reds")
	ax[1,0].set_xlabel("Hi-C")
	ax[1,1].set_xlabel("Recon")
	ax[1,2].set_xlabel("Interp")
	print("CHRO"+str(chro))
	print(spearmanr(mat_contacts[0], mat_contacts[0], axis=None))
	print(spearmanr(mat_contacts[0], mat_full_struc[0], axis=None))
	print(spearmanr(mat_contacts[0], mat_mis_struc[0], axis=None))
	print(spearmanr(mat_contacts[0], mat_contacts[1], axis=None))
	print(spearmanr(mat_contacts[1], mat_full_struc[1], axis=None))
	print(spearmanr(mat_contacts[1], mat_mis_struc[1], axis=None))

	#plt.show()
	plt.savefig("Figures/Cardio/viz_chro_"+str(chro)+"_time_"+str(time))
