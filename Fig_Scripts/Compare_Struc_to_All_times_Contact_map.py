from scipy.stats import spearmanr
from Utils import util as ut
import numpy as np
import matplotlib.pyplot as plt
import pdb


##ARGS
chro  = 13
eta   = 1000
alpha = 0.6
lr    = 0.0001
res   = 50000
step  = 21
rep   = 1
epoch = 400

mis = 2
time =4

reps = [1,2]

mat_contacts    = {}
mat_mis_struc   = {}
mat_full_struc  = {}


DAY_LABELS = ['B','Ba', 'D2', 'D4', 'D6', 'D8', 'ES']
MISS       = [2,4,6,8]
MIS_TIMES  = [4,8,12,16]
CHROS      = [11,12,13,14,15,16,17,18,19]
chro_mis_spears = {}
chro_full_spears = {}


chro_mis_spears = np.load("Fig_Scripts/iPSC_SPC_mis.npy", allow_pickle=True).item()
chro_full_spears = np.load("Fig_Scripts/iPSC_SPC_ful.npy", allow_pickle=True).item()
pdb.set_trace()
for chro in CHROS:
	if chro in chro_mis_spears.keys():
		continue
	for r, rep in enumerate(reps):
		for day in DAY_LABELS:
			CONTACT_STRING  = "Real_Data/iPluripotent/day_"+day+"_rep_"+str(rep)+"_chro_"+str(chro)
			print(CONTACT_STRING)
			mat_contacts[r, day] = ut.loadConstraintAsMat(CONTACT_STRING)

		for m, mis in enumerate(MISS):
			MIS_STRUC_STRING   = "Generated_Structures/ipsc_missing_"+str(mis)+"_rep_"+str(rep)+"_eta_"+str(eta)+"_alpha_"+str(alpha)+"_lr_"+str(lr)+"_epoch_"+str(epoch)+"_res_"+str(res)+"_step_"+str(step)+"_chro_"+str(chro)+".npy"
			FULL_STRUC_STRING   = "Generated_Structures/ipsc_full_rep_"+str(rep)+"_eta_"+str(eta)+"_alpha_"+str(alpha)+"_lr_"    +str(lr)+"_epoch_"+str(epoch)+"_res_"+str(res)+"_step_"+str(step)+"_chro_"+str(chro)+".npy"
			print(MIS_STRUC_STRING)
			mat_mis_struc[r, mis] = ut.loadStrucAtTimeAsMat(MIS_STRUC_STRING, MIS_TIMES[m])
			mat_full_struc[r, mis] = ut.loadStrucAtTimeAsMat(FULL_STRUC_STRING, MIS_TIMES[m])

	mis_spears  = np.zeros((len(reps), len(MISS), len(DAY_LABELS)))
	full_spears = np.zeros((len(reps), len(MISS), len(DAY_LABELS)))
	for r, rep in enumerate(reps):
		for m, mis in enumerate(MISS):
			for d, day in enumerate(DAY_LABELS):
				mis_spears[r,m,d]  = spearmanr(mat_mis_struc[0,mis], mat_contacts[0,day], axis=None)[0]
				full_spears[r,m,d] = spearmanr(mat_full_struc[0,mis], mat_contacts[0,day], axis=None)[0]

	chro_mis_spears[chro]=mis_spears
	chro_full_spears[chro]=full_spears

pdb.set_trace()
np.save("Fig_Scripts/iPSC_SPC_mis",chro_mis_spears)
np.save("Fig_Scripts/iPSC_SPC_ful",chro_full_spears)

