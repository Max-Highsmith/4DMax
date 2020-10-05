from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import procrustes
import numpy as np
import matplotlib.pyplot as plt
import pdb
from Utils import eval_tool as ev

chros = list(range(1,20))
steps = [15,29,43,57,71]
spear_mat   = np.zeros((len(chros),len(steps)))
pear_mat   = np.zeros((len(chros),len(steps)))
for c, chro in enumerate(chros):
	dayOfInterest =5
	for s1, stp1 in enumerate(steps):
		print(str(s1))
		days_a = np.linspace(0,14, 15)
		days_b = np.linspace(0,14, stp1)
		indx   = np.argwhere(days_b ==dayOfInterest)[0][0]
		struca = np.load("Generated_Structures/cardio_full_rep_1_eta_1000_alpha_0.6_lr_0.0001_epoch_400_res_1_step_15_chro_"+str(chro)+".npy")
		strucb = np.load("Generated_Structures/cardio_full_rep_1_eta_1000_alpha_0.6_lr_0.0001_epoch_400_res_1_step_"+str(stp1)+"_chro_"+str(chro)+".npy")
		
		mtx1, mtx2, disparity = procrustes(struca[dayOfInterest], strucb[indx])
		print(disparity)
		'''
		#DO NOT DELETE THIS PRODUCES FIG6c
		fig =plt.figure()
		ax = fig.add_subplot(111, projection='3d')
		ax.plot(mtx1[:,0], mtx1[:,1], mtx1[:,2], color="cornflowerblue", label="Granularity 15")
		ax.plot(mtx2[:,0], mtx2[:,1], mtx2[:,2], color="maroon", label="Granularity "+str(stp1))
		ax.legend()
		plt.show()
		'''
		spear, pear  = ev.compare4D_Diff_gran(struca, strucb, 0,14)
		#print(np.mean(comp))
		spear_mat[c,s1] = np.mean(spear)
		pear_mat[c,s1] = np.mean(pear)

fig, ax = plt.subplots(1)
spear_mat = np.transpose(spear_mat)
ax.imshow(spear_mat, cmap="Greens", vmin=0, vmax=1)

for (j,i), label in np.ndenumerate(spear_mat):
	ax.text(i,j,"{:.2f}".format(label), ha='center', va='center', color='white')

ax.set_xticks([])
ax.set_yticks([])
plt.show()

fig, ax = plt.subplots(1)
pear_mat = np.transpose(pear_mat)
ax.imshow(pear_mat, cmap="Greens", vmin=0, vmax=1)

for (j,i), label in np.ndenumerate(pear_mat):
	ax.text(i,j,"{:.2f}".format(label), ha='center', va='center', color='white')

ax.set_xticks([])
ax.set_yticks([])
plt.show()

pdb.set_trace()
'''
fig, ax = plt.subplots(1)
for s, step in enumerate(steps):
	ax.plot(mat[:,s], label=str(step))
	ax.set_xticklabels(chros)
	ax.set_yt

#ax.set_xticks(list(range(0,len(steps))))
#ax.set_xticklabels(steps)
#ax.set_xlabel("Step")
plt.show()
'''
