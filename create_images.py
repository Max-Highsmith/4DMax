import os
import pdb
import matplotlib.pyplot as plt
import numpy as np

OUT_DIR      = "Image_Results/load"
STRUC_FILE   = "Generated_Structures/PSC_rep1_1.npy"
TIME_POINTS  = np.linspace(0,5,21)
def plot3d(struc, timepoints, dirr):
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
		x   = struc[t][:,0]
		y   = struc[t][:,1]
		z   = struc[t][:,2]
		ax.plot(x,y,z, linewidth=1)
		ax.set_title(str(TIME_POINTS[t]))
		ax.set_xlim(window[0], window[1])
		ax.set_ylim(window[0], window[1])
		ax.set_zlim(window[0], window[1])
		plt.savefig(dirr+"/"+str(t)+".png")

if not os.path.isdir(OUT_DIR):
	os.makedirs(OUT_DIR)
structure = np.load(STRUC_FILE)
plot3d(structure, TIME_POINTS,OUT_DIR)
os.system("./make_real_gif.sh "+str(structure.shape[0]-1)+" "+str(OUT_DIR)+" fig.gif")
