from scipy.stats import pearsonr
import functools
import time
import matplotlib.pyplot as plt
import pdb
import torch
import numpy as np

np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

#lr    = .001
alpha  = 0.6
epochs = 50
#res    = 50000
res = 1
lr = .000001
#lr     = .00001
#res  = 50000


def pcc_distances(hic_dist, wish_dist):
	#al = np.corrcoef(hic_dist, wish_dist)	
	val = pearsonr(hic_dist, wish_dist)
	print(val)

def show_struc(structure, e, n_min):
	fig    = plt.figure()
	ax     = plt.axes(projection="3d")
	x      = structure[:,0]
	y      = structure[:,1]
	z      = structure[:,2]
	ax.plot(x,y,z, linewidth=1)
	#for i in range(0,100):
		#ax.text(x[i],y[i],z[i], str(i))
	#for i in range(1700,x.shape[0]):
	#	ax.text(x[i],y[i],z[i], str(i))
	plt.show() 

def if2dist(contact_maps):
	#alpha = 1
	return 1/(contact_maps**alpha)

def getWishDist(struc, row, col):
	start = time.time()
	n     = row.shape[0]
	wish  = np.zeros(row.shape)
	wish  = np.linalg.norm(struc[row]-struc[col],axis=1)
	#print("wish time", time.time()-start)
	return wish
			

def getGradient(hic_dist, row, col, struc):
	start_time = time.time()
	wish_dist = getWishDist(struc, row, col)
	n = hic_dist.shape[0]
	v = 0
	dl_ddk   = np.zeros(hic_dist.shape)
	ddk_dxyz = np.zeros((hic_dist.shape[0], 3))
	#print("time a", time.time()-start_time)
	start_time = time.time()

	diff = np.abs(wish_dist-hic_dist)
	v    = np.sum(diff)
	#print("time b",time.time()-start_time)
	start_time = time.time()
	
	dl_ddk = (n*(hic_dist-wish_dist))/v
	denoms = np.linalg.norm(struc[row]-struc[col], axis=1)
	ddk_dxyz = ((struc[row]-struc[col]).transpose()/denoms).transpose()
	ddk_dxyz[np.abs(denoms)<.001] = np.zeros(3)
	#print("alt c",time.time()-start_time)
	start_time = time.time()
	return dl_ddk, ddk_dxyz

#day_0     = np.loadtxt("norm_VC_res_50000_chr_1.txt")
#day_0     = np.loadtxt("Synthetic_Data/Synthetic_Contact_Maps/struc1_3.txt")
#day_0     = np.loadtxt("day_0_chr_9.txt")
#day_0     = np.loadtxt("Real Data/chr1_100000.txt")
day_0      = np.loadtxt("Real_Data/iPluripotent/day_D2_rep_1_chro_18")
#day_0     = np.loadtxt("Real_Data/Cardiomyocyte/GSM2845448_ESC_Rep1_500KB_ICED.matrix")


row        = (day_0[:,0].astype(int)/res).astype(int)
col        = (day_0[:,1].astype(int)/res).astype(int)
n_max      = np.max((row,col))
n_min      = np.min((row,col))
ifs        = day_0[:,2]
hic_dist   = if2dist(ifs)
np.random.seed(0)
struc      = np.random.rand(n_max+1-n_min, 3)

row        = row-n_min
col	   = col-n_min


prev_struc = struc
wish_dist  = getWishDist(struc, row, col)
prev_time=time.time()
for e in range(0, epochs):
	print(e)
	start_time = time.time()
	dl_ddk, ddk_dxyz  = getGradient(hic_dist, row, col, prev_struc)
	#print("getGrad", time.time()-start_time)
	start_time = time.time()

	change       = np.zeros(prev_struc.shape)
	changea      = np.zeros(prev_struc.shape)
	changeb      = np.zeros(prev_struc.shape)
	grada        = (ddk_dxyz.transpose()*dl_ddk).transpose()
	gradb        = -(ddk_dxyz.transpose()*dl_ddk).transpose()
	for i in range(0,3):
		#changea[:,i] = np.bincount(row, weights=grada[:,i], minlength=n_max+1)
		#changeb[:,i] = np.bincount(col, weights=gradb[:,i], minlength=n_max+1)
		changea[:,i] = np.bincount(row, weights=grada[:,i], minlength=n_max-n_min+1)
		changeb[:,i] = np.bincount(col, weights=gradb[:,i], minlength=n_max-n_min+1)

	change          = changea+changeb
	prev_struc     += lr*change
	
	#current match
	wish_dist = getWishDist(struc, row, col)
	pcc_distances(hic_dist, wish_dist)
	print("change time", time.time()-start_time)
show_struc(prev_struc, 0, n_min)

