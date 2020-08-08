import os
import pdb
import numpy as np
import matplotlib.pyplot as plt

TAD="_TAD"
RES="res_150"
SET="set_3"
times = 100

SETS = ["set_0","set_1","set_2","set_3","set_4","set_5","set_6"]
TADS = ["_TAD", ""]
RESS = ["res_150", "res_40", "res_75"]

for TAD in TADS:
	for RES in RESS:
		for SET in SETS:
			FN = "Synthetic_Data/20150115_Trussart_Dataset" \
				"/Toy_Models/"+str(RES)+str(TAD)+"/"\
				""+str(SET)+'/model_10.xyz'
			x = np.loadtxt(FN, skiprows=2)
			x.shape[0]
			struc = np.zeros((times ,x.shape[0], 3))

			for i in range(1, times+1):
				FN = "Synthetic_Data/20150115_Trussart_Dataset" \
				"/Toy_Models/"+str(RES)+str(TAD)+"/"\
				""+str(SET)+"/model_"+str(i)+".xyz"
				x = np.loadtxt(FN, skiprows=2)
				struc[i-1]=x[:,1:]


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
					fig.set_size_inches(14,10)
					x   = struc[t][:,0]
					y   = struc[t][:,1]
					z   = struc[t][:,2]
					ax.plot(x,y,z, linewidth=1)
					ax.set_xlim(window[0], window[1])
					ax.set_ylim(window[0], window[1])
					ax.set_zlim(window[0], window[1])
					plt.savefig(dirr+"/"+str(t)+".png")

			plot3d(struc, list(range(0,100)), "Synthetic_Data/Trussart_Images" )
			OUT_DIR = "Synthetic_Data/Trussart_Images"
			os.system("./make_real_gif.sh "+str(struc.shape[0]-1)+" "+str(OUT_DIR)+" "+"Gifs/Trussart/trusart"+str(SET)+str(TAD)+str(RES)+".gif")
