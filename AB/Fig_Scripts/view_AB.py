import numpy as np
import matplotlib.pyplot as plt
import pdb

ETA     = 1000
ALPHA   = 0.6
RES     = 50000
STEP    = 21
MISSING = 2
EPOCH   = 400
LR      = "0.0001"

CHRO  = 13
REP   = 1
DAYS  = ['B', 'D2', 'D4','D6','D8','ES']
TIMES = [  0,    4,    8,  12,  16, 20]
real  = {}

for d, day in enumerate(DAYS):
	real[day] = np.load("AB_Vecs/real_ipsc_day_"+str(day)+"_rep_"+str(REP)+"_chro_"+str(CHRO)+".npy")

model = np.load("AB_Vecs/struc_ipsc_missing_"+str(MISSING)+"_rep_"+str(REP)+"_eta_"+str(ETA)+"_alpha_"+str(ALPHA)+"_lr_"+str(LR)+"_epoch_"+str(EPOCH)+"_res_"+str(RES)+"_step_"+str(STEP)+"_chro_"+str(CHRO)+".npy")

fig, ax = plt.subplots(len(TIMES))
for t, time in enumerate(TIMES):
	ax[t].bar(list(range(0, model[time].shape[0])), model[time], label=str(time), color='cornflowerblue')
ax[0].set_title("struc")
fig, ax = plt.subplots(len(DAYS))
for d, day in enumerate(DAYS):
	ax[d].bar(list(range(0,real[day].shape[0])), real[day], label=day, color="peru")
	ax[d].set_xlabel(day)
plt.show()
