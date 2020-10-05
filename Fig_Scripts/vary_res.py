from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import procrustes
from Utils import eval_tool as ev
import pdb
import numpy as np
import matplotlib.pyplot as plt

def condenseStruc4D(struc, factor):
	newsize  = int(struc.shape[1]/factor)-1
	newstruc = np.zeros((struc.shape[0], newsize, 3))
	for t in range(0, struc.shape[0]):
		for i in range(0, newstruc.shape[1]):
			newstruc[t,i,0] = np.mean(struc[t,int(i*factor):int((i*factor)+factor),0])
			newstruc[t,i,1] = np.mean(struc[t,int(i*factor):int((i*factor)+factor),1])
			newstruc[t,i,2] = np.mean(struc[t,int(i*factor):int((i*factor)+factor),2])
	return newstruc

plot_spear = []
plot_pears = []
chros = list(range(1,20))
for chro in chros:
	scal_factor = 10
	struca        = np.load("Generated_Structures/ipsc_full_rep_1_eta_1000_alpha_0.6_lr_0.0001_epoch_400_res_50000_step_21_chro_"+str(chro)+".npy")
	strucb        = np.load("Generated_Structures/ipsc_small_rep_1_eta_1000_alpha_0.6_lr_0.0001_epoch_400_res_500000_step_21_chro_"+str(chro)+".npy")
	struca_shrink = condenseStruc4D(struca, scal_factor)
	minn = min(strucb.shape[1], struca_shrink.shape[1])
	struca_shrink = struca_shrink[:,:minn,:]
	strucb        = strucb[:,:minn,:]
	spears, conext = ev.compare4D(struca_shrink, strucb)
	print(spears)
	plot_spear.append(spears[0])
	plot_pears.append(spears[1])
	for indx in range(0,21):
		mtx1, mtx2, disparity = procrustes(struca_shrink[indx], strucb[indx])
		pear, spear = ev.compare3D(struca_shrink[indx], strucb[indx])
		print("indx:"+str(indx)+"\tdisparity:"+str(disparity)+"\tpear:"+str(pear)+"\tspear"+str(spear))
		fig = plt.figure()
		ax  = fig.add_subplot(111, projection='3d')
		ax.plot(mtx1[:,0], mtx1[:,1], mtx1[:,2], color="mediumpurple", label="res 50k")
		ax.plot(mtx2[:,0], mtx2[:,1], mtx2[:,2], color="seagreen", label="res 500k")
		ax.legend()
		plt.savefig("Figures/change_res/ipsc_"+str(chro)+"_indx_"+str(indx)+"_.png")
		plt.close()
		plt.clf()
fig, ax = plt.subplots(1)
ax.plot(plot_spear, color='limegreen')
ax.plot(plot_pears, color='blueviolet')
ax.set_xlabel("")
ax.set_ylabel("")
ax.set_xticks(np.array(chros)-1)
ax.set_xticklabels(chros)
ax.set_xlabel("Chros")
ax.set_ylabel("Correlation")
ax.set_title("avg Correlation 500kb vs 50kb")
print("spear: mean:"+str(np.mean(plot_spear))+"\t max"+str(np.max(plot_spear))+"\t"+str(np.argmax(plot_spear)))
print("pearson: mean:"+str(np.mean(plot_pears))+"\t max"+str(np.max(plot_pears))+"\t"+str(np.argmax(plot_pears)))
ax.legend()
plt.show()

pdb.set_trace()
