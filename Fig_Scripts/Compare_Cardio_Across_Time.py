import glob
from sklearn.decomposition import PCA
import sys
import numpy.ma as ma
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
res   = 1
step  = 15
rep   = 1
epoch = 400

reps = [1,2]

mat_contacts   = {}
mat_mis_struc  = {}
mat_full_struc = {}
rep = 1

for chro in list(range(13,14)):
	print(chro)
	FULL_STRUC_STRING   = "Generated_Structures/cardio_full_rep_"+str(rep)+"_eta_"+str(eta)+"_alpha_"+str(alpha)+"_lr_"+str(lr)
	FULL_STRUC_STRING  += "_epoch_"+str(epoch)+"_res_"+str(res)+"_step_"+str(step)+"_chro_"+str(chro)+".npy"

	for t, (time,day) in enumerate(zip([0,2,5,14], ['ESC', 'MES', 'CP','CM'])):
		mat_full_struc[t]    = ut.loadStrucAtTimeAsMat(FULL_STRUC_STRING,time)
		CONTACT_STRING       = "Real_Data/Cardiomyocyte/RUES2/By_Chros/*_"+str(day)+"_Rep"+str(rep)+"_500KB_"+str(chro)
		CONTACT_STRING       =glob.glob(CONTACT_STRING)[0]
		mat_contacts[t]      = ut.loadConstraintAsMat(CONTACT_STRING, res=1)

	pdb.set_trace()
	##
	## compute ab
	fig, ax = plt.subplots(2,4)
	for t, time in enumerate([0,2,5,14]):
		spear = spearmanr(mat_full_struc[t], mat_contacts[t], axis=None)
		print(spear)
		ax[0,t].imshow(np.clip(mat_full_struc[t], 0,10), cmap="PuBuGn")
		ax[1,t].imshow(np.clip(mat_contacts[t], 0,30), cmap="YlOrRd")
		ax[0,t].set_title(str(time))
		ax[0,t].set_xticks([])
		ax[1,t].set_xticks([])
		ax[0,t].set_yticks([])
		ax[1,t].set_yticks([])


	fig.suptitle("Chro "+str(chro))
	plt.savefig("Figures/Cardio/Time_Contacts/timecontacts_chro_"+str(chro)+".png")
	plt.clf()
	plt.close()
	plt.cla()

	spears = np.zeros((4,4))
	for i, itime in enumerate([0,2,5,14]):
		for j, jtime in enumerate([0,2,5,14]):
			spears[i,j] = spearmanr(mat_full_struc[i], mat_contacts[j], axis=None)[0]

	fig, ax = plt.subplots(1)
	ax.imshow(spears, cmap="Greys")
	for (j,i), label in np.ndenumerate(spears):
		ax.text(i,j,"{:.2f}".format(label), ha='center', va='center', color='Red', size=20)
		
	ax.set_xticks([0,1,2,3])
	ax.set_yticks([0,1,2,3])
	ax.set_xticklabels(['ESC','MES','CP','CM'])
	ax.set_yticklabels(['ESC','MES','CP','CM'])
	ax.set_xlabel("Recon Map")
	ax.set_ylabel("Real Map")
	ax.set_title("Chro "+str(chro))
	plt.savefig("Figures/Cardio/Full_Heatmaps/heat_chro_"+str(chro)+".png")
	plt.clf()
	plt.close()
	plt.cla()

