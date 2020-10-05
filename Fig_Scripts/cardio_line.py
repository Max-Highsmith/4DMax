import glob
from scipy.stats import spearmanr
from Utils import util as ut
import numpy as np
import matplotlib.pyplot as plt
import pdb


##ARGS
rep   = 1
epoch = 400

#cardio these are the same
mis = 2
time =2

reps = [1,2]

CHROS = list(range(1,23))
mis_spc = []
ful_spc = []
rep_spc = []
for chro in CHROS:
	print(chro)
	mat_contacts   = {}
	mat_mis_struc  = {}
	mat_full_struc = {}

	for r, rep in enumerate(reps):
		FULL_STRUC_STRING   = "Generated_Structures/cardio_full_rep_"+str(rep)+"_eta_1000_alpha_0.6_lr_0.0001_epoch_400_res_1_step_15_chro_"+str(chro)+".npy"
		MIS_STRUC_STRING    = "Generated_Structures/cardio_missing_2_rep_"+str(rep)+"_eta_1000_alpha_0.6_lr_0.0001_epoch_400_res_1_step_15_chro_"+str(chro)+".npy"
		CONTACT_STRING      = "Real_Data/Cardiomyocyte/RUES2/By_Chros/*_MES_Rep"+str(rep)+"_500KB_"+str(chro)
		CONTACT_STRING = glob.glob(CONTACT_STRING)[0]
		mat_contacts[r]      = ut.loadConstraintAsMat(CONTACT_STRING, res=1)
		mat_mis_struc[r]     = ut.loadStrucAtTimeAsMat(MIS_STRUC_STRING, time)
		mat_full_struc[r]    = ut.loadStrucAtTimeAsMat(FULL_STRUC_STRING,time)

	mis_spc.append(spearmanr(mat_contacts[0], mat_mis_struc[0], axis=None)[0])
	ful_spc.append(spearmanr(mat_contacts[0], mat_full_struc[0], axis=None)[0])
	rep_spc.append(spearmanr(mat_contacts[0], mat_contacts[1], axis=None)[0])

fig, ax = plt.subplots(1)
ax.plot(mis_spc, CHROS,label="Interp", color="darkorange")
ax.plot(rep_spc, CHROS,label="Rep", color="cornflowerblue")
ax.plot(ful_spc, CHROS,label="Recon", color="palegreen")
ax.set_yticks(CHROS)
ax.set_title("Interpolation Day"+str(time))
plt.legend()
plt.savefig("Figures/Cardio/Interp_lines/line_time_"+str(time)+".png")

numBetter = 0
for i, val in enumerate(rep_spc):
	if mis_spc[i] > rep_spc[i]:
		numBetter = numBetter + 1
	
print("Better than Biological replicate:", str(numBetter/len(rep_spc)))
pdb.set_trace()

