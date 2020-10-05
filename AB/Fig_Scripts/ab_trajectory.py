import pdb
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline
from scipy.stats import spearmanr
from sklearn.decomposition import PCA
days  = ['B','D2','D4','D6','D8','ES']
times = [0,  4,   8,   12,  16,  20]
real  = {}
struc = {}
#chro=2
chros = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
SIGN = True 

for SIGN in [True, False]:
	for chro in chros:
		vec_dim =np.load("Full_AB_Vecs/real_vec_day_B_chro_"+str(chro)+".npy").shape[0]
		real   = np.zeros((len(days), vec_dim))
		struc  = np.zeros((len(days), vec_dim))

		for d, day in enumerate(days):
			real[d]  = np.load("Full_AB_Vecs/real_vec_day_"+str(day)+"_chro_"+str(chro)+".npy")
			spear = spearmanr(real[0],real[d])[0]
			if spear <0:
				real[d] = (-1)*real[d]

		for t, time in enumerate(times):
			struc[t]  = np.load("Full_AB_Vecs/struc_vec_time_"+str(time)+"_chro_"+str(chro)+".npy")
			spear = spearmanr(real[0],struc[t])[0]
			if spear <0:
				struc[t] = (-1)*struc[t]

		if SIGN == True:
			for t, time in enumerate(times):
				struc[t] = np.sign(struc[t])
			for d, day in enumerate(days):
				real[d]  = np.sign(real[d])

		fig, ax = plt.subplots(2*len(days), figsize=(10,10))
		for i, (day, time) in enumerate(zip(days,times)):
			ax[2*i  ].bar(list(range(0,  real[i].shape[0])), real[i], color="red")
			ax[2*i+1].bar(list(range(0, struc[i].shape[0])), struc[i], color="blue")
			#ax[2*i].set_axis_off()
			#ax[2*i+1].set_axis_off()
			ax[2*i].set_xticks([])
			ax[2*i+1].set_xticks([])
			ax[2*i].set_yticks([])
			ax[2*i+1].set_yticks([])
			ax[2*i].set_ylabel("Real:"+str(day))
			ax[2*i+1].set_ylabel("Recon:"+str(day))

		plt.savefig("Figs/AB_Rows/row_chro_"+str(chro)+"_sign_"+str(SIGN)+".png")
		plt.clf()
		plt.cla()
		plt.close()

		combo = np.vstack((real,struc))
		pca     = PCA(n_components=2)
		ab = pca.fit_transform(combo)
		pca_vals = pca.explained_variance_ratio_
		fig, ax = plt.subplots(1)
		ax.scatter(ab[:,0],ab[:,1], color="purple")

		ax.plot(ab[0:len(days),0], ab[0:len(days),1], color="red")
		ax.plot(ab[len(days):,0], ab[len(days):,1], color="blue")
		ax.set_xlabel("PC1 ("+"{:.2f}".format(100*pca_vals[0])+"%)")
		ax.set_ylabel("PC2 ("+"{:.2f}".format(100*pca_vals[1])+"%)")
		ax.set_xticks([])
		ax.set_yticks([])
		ax.spines['right'].set_visible(False)
		ax.spines['top'].set_visible(False)
		lab_strings = ['Real B','Real D2','Real D4','Real D6','Real D8','Real PSC','Recon B','Recon D2', 'Recon D4', 'Recon D6', 'Recon D8', 'Recon PSC']
		for i, txt in enumerate(lab_strings):
			plt.annotate(txt, (ab[i,0], ab[i,1]))
		plt.savefig("Figs/Trajectories/traj_chro_"+str(chro)+"_sign_"+str(SIGN)+".png")
		plt.close()
		plt.cla()
		plt.clf()
