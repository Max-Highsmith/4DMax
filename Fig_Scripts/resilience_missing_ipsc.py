import numpy as np
import matplotlib.pyplot as plt
import pdb
import sys
from Utils import eval_tool as ev

'''
chros = list(range(1,20))
full_sp =[]
full_pe =[]
full_s_c=[]
full_p_c=[]
for chro in chros:
	miss     = [2,4,6,8]
	stria    = "Generated_Structures/ipsc_full_rep_1_eta_1000_alpha_0.6_lr_0.0001_epoch_400_res_50000_step_21_chro_"+str(chro)+".npy"
	struca   = np.load(stria)
	spears   = []
	pears    = []
	s_cons    = []
	p_cons    = []
	for mis in miss:
		print(mis)
		strib  = "Generated_Structures/ipsc_missing_"+str(mis)+"_rep_1_eta_1000_alpha_0.6_lr_0.0001_epoch_400_res_50000_step_21_chro_"+str(chro)+".npy"
		strucb = np.load(strib)
		if struca.shape[1] != strucb.shape[1]:
			minn = min(struca.shape[1], strucb.shape[1])
			struca = struca[:minn,:minn]
			strucb = strucb[:minn,:minn]
		(spear,pear), (s_con, p_con)    = ev.compare4D(struca, strucb)
		spears.append(spear)
		pears.append(pear)
		s_cons.append(s_con[0])
		p_cons.append(p_con[0])
	full_sp.append(spears)
	full_pe.append(pears)
	full_s_c.append(s_cons)
	full_p_c.append(p_cons)
pdb.set_trace()
full_sp = np.array(full_sp)
full_pe = np.array(full_pe)
full_s_c = np.array(full_s_c)
full_p_c = np.array(full_p_c)
fig, ax = plt.subplots(2)

ax[0].set_xticklabels(chros)
ax[1].set_xticklabels(chros)
ax[0].set_xticks(np.array(chros)-1)
ax[1].set_xticks(np.array(chros)-1)
ax[0].set_xlabel("Chros")
ax[1].set_xlabel("Chros")
ax[0].set_title("4DModel similarity SPC")
ax[1].set_title("4DModel similarity PCC")

for m, mis in enumerate(miss):
	ax[0].plot(full_sp[:,m], label=str(mis))
	ax[1].plot(full_pe[:,m], label=str(mis))
ax[0].plot(full_s_c[:,m], label=str("context"))
ax[1].plot(full_p_c[:,m], label=str("context"))
ax[1].legend()
plt.savefig("Figures/iPSC/4DModel_Sim/ipsc_mis_resil.png")

'''

miss     = [2]
chros = list(range(1,22))
full_sp =[]
full_pe =[]
full_s_c=[]
full_p_c=[]
for chro in chros:
	miss     = [2]
	stria    = "Generated_Structures/cardio_full_rep_1_eta_1000_alpha_0.6_lr_0.0001_epoch_400_res_1_step_15_chro_"+str(chro)+".npy"
	struca   = np.load(stria)
	spears   = []
	pears    = []
	s_cons    = []
	p_cons    = []
	for mis in miss:
		print(mis)
		strib  = "Generated_Structures/cardio_missing_2_rep_1_eta_1000_alpha_0.6_lr_0.0001_epoch_400_res_1_step_15_chro_"+str(chro)+".npy"
		strucb = np.load(strib)
		if struca.shape[1] != strucb.shape[1]:
			minn = min(struca.shape[1], strucb.shape[1])
			struca = struca[:minn,:minn]
			strucb = strucb[:minn,:minn]
		(spear,pear), (s_con, p_con)    = ev.compare4D(struca, strucb)
		spears.append(spear)
		pears.append(pear)
		s_cons.append(s_con[0])
		p_cons.append(p_con[0])
	full_sp.append(spears)
	full_pe.append(pears)
	full_s_c.append(s_cons)
	full_p_c.append(p_cons)
pdb.set_trace()
full_sp = np.array(full_sp)
full_pe = np.array(full_pe)
full_s_c = np.array(full_s_c)
full_p_c = np.array(full_p_c)
fig, ax = plt.subplots(2)

ax[0].set_xticklabels(chros)
ax[1].set_xticklabels(chros)
ax[0].set_xticks(np.array(chros)-1)
ax[1].set_xticks(np.array(chros)-1)
ax[0].set_xlabel("Chros")
ax[1].set_xlabel("Chros")
ax[0].set_title("4DModel similarity SPC")
ax[1].set_title("4DModel similarity PCC")

for m, mis in enumerate(miss):
	ax[0].plot(full_sp[:,m], label=str(mis))
	ax[1].plot(full_pe[:,m], label=str(mis))
ax[0].plot(full_s_c[:,m], label=str("context"))
ax[1].plot(full_p_c[:,m], label=str("context"))
ax[1].legend()
plt.show()
plt.savefig("Figures/Cardio/4DModel_Sim/cardio_mis_resil.png")


