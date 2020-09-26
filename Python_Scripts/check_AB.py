from Utils import util as ut
import numpy as np
import pdb 
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

colors = ['orange','goldenrod','yellow','darkkhaki','green', 'turquoise']
chros = [15,16,17,18,19]
for chro in chros:
	plt.close()
	plt.cla()
	plt.clf()
	fig, ax    = plt.subplots(6,4, figsize=(20,10))
	for j, mis in enumerate([2,4,6,8]):
		struc      = np.load("Generated_Structures/ipsc_missing_"+str(mis)+"_rep_2_eta_1000_alpha_0.6_lr_0.0001_epoch_400_res_50000_step_21_chro_"+str(chro)+".npy")
		for i, (t,day) in enumerate(zip([0,4,8,12,16,20],[0,2,4,6,8,10])):
			print(str(i), str(j))
			struc_snap = struc[t]
			contact    = ut.struc2contacts(struc_snap)
			pear       = np.corrcoef(np.log(contact))
			pca        = PCA(n_components=1)
			AB         = pca.fit_transform(pear)
			ax[i,j].bar(list(range(0, AB.shape[0])), np.squeeze(AB), color=colors[i] )
			ax[i,j].set_yticks([-.5,.5])
			ax[i,j].set_yticklabels(['B','A'])
			ax[i,j].set_ylabel(str(day))
			ax[i,j].set_xlabel(str(mis))
	plt.savefig("pca"+str(chro)+".png")


pdb.set_trace()
