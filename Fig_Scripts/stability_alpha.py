from scipy import stats
from scipy.spatial import procrustes
import numpy as np
import matplotlib.pyplot as plt
import pdb
from mpl_toolkits.mplot3d import Axes3D
import sys
from Utils import eval_tool as ev

alphas = [0.2, 0.4, 0.6, 0.8, 1.0]
fig = plt.figure()
ax  = fig.add_subplot(111, projection='3d')
indx = 0

def clean(x,y,z):
	x_score = np.abs(stats.zscore(x))
	y_score = np.abs(stats.zscore(y))
	z_score = np.abs(stats.zscore(z))
	threshold = 3 
	toRemove = np.hstack((np.where(x_score>3), np.where(y_score>3), np.where(z_score>3)))
	toRemove = np.unique(toRemove)
	xclean   = np.delete(x,toRemove)
	yclean   = np.delete(y,toRemove)
	zclean   = np.delete(z,toRemove)    
	return xclean, yclean, zclean

def clean2(struca, strucb):
	x1 = struca[:,0]
	y1 = struca[:,1]
	z1 = struca[:,2]
	x2 = strucb[:,0]
	y2 = strucb[:,1]
	z2 = strucb[:,2]
	x_score1 = np.abs(stats.zscore(x1))
	y_score1 = np.abs(stats.zscore(y1))
	z_score1 = np.abs(stats.zscore(z1))
	x_score2 = np.abs(stats.zscore(x2))
	y_score2 = np.abs(stats.zscore(y2))
	z_score2 = np.abs(stats.zscore(z2))
	threshold = 3 
	toRemove = np.hstack((np.where(x_score1>threshold),
				 np.where(y_score1>threshold),
				 np.where(z_score1>threshold),
				 np.where(x_score2>threshold),
				 np.where(y_score2>threshold),
				 np.where(z_score2>threshold)))
	toRemove = np.unique(toRemove)
	x1clean   = np.delete(x1,toRemove)
	y1clean   = np.delete(y1,toRemove)
	z1clean   = np.delete(z1,toRemove)    
	x2clean   = np.delete(x2,toRemove)
	y2clean   = np.delete(y2,toRemove)
	z2clean   = np.delete(z2,toRemove)    
	struc1 = np.transpose(np.array((x1clean, y1clean, z1clean)))
	struc2 = np.transpose(np.array((x2clean, y2clean, z2clean)))
	return struc1, struc2




for alpha in alphas:
	stri_base   = "Generated_Structures/cardio_full_rep_1_eta_1000_alpha_0.4_lr_0.0001_epoch_400_res_1_step_15_chro_10.npy"
	stri        = "Generated_Structures/cardio_full_rep_1_eta_1000_alpha_"+str(alpha)+"_lr_0.0001_epoch_400_res_1_step_15_chro_10.npy"
	struc       = np.load(stri)
	struc_base  = np.load(stri_base)
	struc_clean, struc_clean_base = clean2(struc[indx], struc_base[indx])
	#struc_clean = np.transpose(np.array(clean(struc[indx][:,0], struc[indx][:,1], struc[indx][:,2])))
	#struc_clean_base = np.transpose(np.array(clean(struc_base[indx][:,0], struc_base[indx][:,1], struc_base[indx][:,2])))
	mtx1, mtx2, disparity = procrustes(struc_clean, struc_clean_base)
	fig = plt.figure()
	ax  = fig.add_subplot(111, projection='3d')
	ax.plot(mtx1[:,0],mtx1[:,1], mtx1[:,2], color="purple")
	ax.plot(mtx2[:,0],mtx2[:,1], mtx2[:,2], color="blue")
	plt.show()
	
