from sklearn.decomposition import PCA
import sys
import numpy.ma as ma
from scipy.stats import spearmanr
from Utils import util as ut
import numpy as np
import matplotlib.pyplot as plt
import pdb


fig, ax = plt.subplots(2,6, gridspec_kw={'wspace':0.0, 'hspace':0.0})
chros = [13,19]#list(range(1,20))
for chro in chros:
	print(chro)
	##ARGS
	#chro  = 18
	eta   = 1000
	alpha = 0.6
	lr    = 0.0001
	res   = 50000
	step  = 21
	rep   = 1
	epoch = 400
	reps = [1,2]

	mat_contacts   = {}
	mat_mis_struc  = {}
	mat_full_struc = {}

	rep = 1
	FULL_STRUC_STRING   = "Generated_Structures/ipsc_full_rep_"+str(rep)+"_eta_"+str(eta)+"_alpha_"+str(alpha)+"_lr_"+str(lr)
	FULL_STRUC_STRING  += "_epoch_"+str(epoch)+"_res_"+str(res)+"_step_"+str(step)+"_chro_"+str(chro)+".npy"

	for t, (time,day) in enumerate(zip([0,4,8,12,16,20], ['B','D2','D4','D6','D8','ES'])):
		mat_full_struc[t]    = ut.loadStrucAtTimeAsMat(FULL_STRUC_STRING,time)
		CONTACT_STRING = "Real_Data/iPluripotent/day_"+str(day)+"_rep_"+str(rep)+"_chro_"+str(chro)
		mat_contacts[t]      = ut.loadConstraintAsMat(CONTACT_STRING)
	
	for d, day in enumerate(['B','D2','D4','D6','D8','ES']):
		for t, time in enumerate([0,4,8,12,16,20]):
			print(str(day)+"/"+str(time)+":"+str(spearmanr(mat_full_struc[t], mat_contacts[d], axis=None)[0]))
				


	fig, ax = plt.subplots(2,6, gridspec_kw={'wspace':0.0, 'hspace':0.0})
	for t, time in enumerate([0,4,8,12,16,20]):
		ax[0,t].imshow(np.clip(mat_full_struc[t], 0,10), cmap="PuBuGn")
		ax[1,t].imshow(np.clip(mat_contacts[t], 0,30), cmap="YlOrRd")
		ax[0,t].set_xticks([])
		ax[1,t].set_xticks([])
		ax[0,t].set_yticks([])
		ax[1,t].set_yticks([])

	fig.suptitle("Chro "+str(chro))
	plt.savefig("Figures/iPSC/Time_Contacts/timecontacts_chro_"+str(chro)+".png")

	spears = np.zeros((6,6))

	def getsize(n):
		return mat_contacts[n].shape[0]

	small = np.min(list(map(getsize,[1,2,3,4,5])))

	for i, itime in enumerate([0,4,8,12,16,20]):
		for j, jtime in enumerate([0,4,8,12,16,20]):
			spears[i,j] = spearmanr(mat_full_struc[i][:small, :small], mat_contacts[j][:small, :small], axis=None)[0]

	fig, ax = plt.subplots(1)
	ax.imshow(spears, cmap="Greys")
	for (j,i), label in np.ndenumerate(spears):
		ax.text(i,j,"{:.2f}".format(label), ha='center', va='center', color='Red')

	ax.set_xticks([0,1,2,3,4,5])
	ax.set_yticks([0,1,2,3,4,5])
	ax.set_yticklabels(['B','D2','D4','D6','D8','PSC'])
	ax.set_xticklabels(['B','D2','D4','D6','D8','PSC'])
	ax.set_xlabel("Recon Map")
	ax.set_ylabel("Real Map")
	ax.set_title("Chro "+str(chro))
	plt.savefig("Figures/iPSC/Full_Heatmaps/heat_chro_"+str(chro)+".png")
	plt.clf()
	plt.close()
	plt.cla()

