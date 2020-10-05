import glob
from scipy.stats import spearmanr
from Utils import util as ut
import numpy as np
import matplotlib.pyplot as plt
import pdb


##ARGS
eta   = 1000
alpha = 0.6
lr    = 0.0001
res   = 50000
step  = 21
rep   = 1
epoch = 400

mis = 2
time =4

miss  = [2,4,6,8]
times = [4,8,12,16]

reps = [1,2]

CHROS = list(range(1,20))
for mis, time in zip(miss, times):
	mis_spc = []
	ful_spc = []
	rep_spc = []
	for chro in CHROS:
		print(chro)
		mat_contacts   = {}
		mat_mis_struc  = {}
		mat_full_struc = {}

		#fig, ax = plt.subplots(ncols=3, nrows=2)
		for r, rep in enumerate(reps):
			FULL_STRUC_STRING   = "Generated_Structures/ipsc_full_rep_"+str(rep)+"_eta_"+str(eta)+"_alpha_"+str(alpha)+"_lr_"+str(lr)
			FULL_STRUC_STRING  += "_epoch_"+str(epoch)+"_res_"+str(res)+"_step_"+str(step)+"_chro_"+str(chro)+".npy"
			MIS_STRUC_STRING    = "Generated_Structures/ipsc_missing_"+str(mis)+"_rep_"+str(rep)+"_eta_"+str(eta)+"_alpha_"+str(alpha)+"_lr_"+str(lr)
			MIS_STRUC_STRING   += "_epoch_"+str(epoch)+"_res_"+str(res)+"_step_"+str(step)+"_chro_"+str(chro)+".npy"
			CONTACT_STRING      = "Real_Data/iPluripotent/day_D2_rep_"+str(rep)+"_chro_"+str(chro)
			mat_contacts[r]      = ut.loadConstraintAsMat(CONTACT_STRING)
			mat_mis_struc[r]     = ut.loadStrucAtTimeAsMat(MIS_STRUC_STRING, time)
			mat_full_struc[r]    = ut.loadStrucAtTimeAsMat(FULL_STRUC_STRING,time)
		revised_mis  = mat_mis_struc[0][0:mat_contacts[0].shape[0], 0:mat_contacts[0].shape[1]]
		revised_full = mat_full_struc[0][0:mat_contacts[0].shape[0], 0:mat_contacts[0].shape[1]]
		mis_spc.append(spearmanr(mat_contacts[0], revised_mis, axis=None)[0])
		ful_spc.append(spearmanr(mat_contacts[0], revised_full, axis=None)[0])
		rep_spc.append(spearmanr(mat_contacts[0], mat_contacts[1], axis=None)[0])

	fig, ax = plt.subplots(1)
	ax.plot(mis_spc, CHROS,label="Interp", color="darkorange")
	ax.plot(rep_spc, CHROS,label="Rep", color="cornflowerblue")
	ax.plot(ful_spc, CHROS,label="Recon", color="palegreen")
	ax.set_yticks(CHROS)
	plt.legend()
	plt.savefig("Figures/iPSC/lines/line_day_"+str(mis)+".png")
	plt.show()
	numBetter = 0
	for i, val in enumerate(rep_spc):
		if mis_spc[i] > rep_spc[i]:
			numBetter = numBetter +1
	print(numBetter)
pdb.set_trace()
