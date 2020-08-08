import os
import pdb
import matplotlib.pyplot as plt
import numpy as np

def plot3d(struc, timepoints, dirr,ts):
	maxx =0.
	minn =0.
	for t in range(0, struc.shape[0]):
		x = struc[t][:,0]
		y = struc[t][:,1]
		z = struc[t][:,2]
		maxx=np.max((x,y,z,np.repeat(maxx, x.shape[0])))
		minn=np.min((x,y,z,np.repeat(minn, x.shape[0])))
		window = (minn, maxx)
	for t in range(0,struc.shape[0]):
		plt.close()
		plt.clf()
		fig = plt.figure()
		ax  = plt.axes(projection="3d")
		fig.set_size_inches(14,10)
		x   = struc[t][:,0]
		y   = struc[t][:,1]
		z   = struc[t][:,2]
		ax.plot(x,y,z, linewidth=1)
		ax.set_title(ts+" "+str(TIME_POINTS[t]*2))
		ax.set_xlim(window[0], window[1])
		ax.set_ylim(window[0], window[1])
		ax.set_zlim(window[0], window[1])
		#for i in range(0,x.shape[0]):
		#	ax.text(x[i],y[i],z[i], s=str(i))
		plt.savefig(dirr+"/"+str(t)+".png")

rep =2
for rep in [1,2]:
	for i in range(7,11):
		chro         = i
		OUT_DIR      = "Image_Results/chro_"+str(chro)
		#STRUC_FILE   = "Generated_Structures/PSC_rep1_1.npy"
		STRUC_FILE   = "Generated_Structures/iPluripotent_rep_"+str(rep)+"_eta_1000_alpha_0.6_lr_0.0001_epoch_400_res_50000_step_21_chro_"+str(chro)+".npy"
		TIME_POINTS  = np.linspace(0,5,21)
		if not os.path.isdir(OUT_DIR):
			os.makedirs(OUT_DIR)
		structure = np.load(STRUC_FILE)
		plot3d(structure, TIME_POINTS,OUT_DIR, "rep_"+str(rep))
		os.system("./make_real_gif.sh "+str(structure.shape[0]-1)+" "+str(OUT_DIR)+" "+"Gifs/fig_"+str(chro)+"_"+str(rep)+"_.gif")
