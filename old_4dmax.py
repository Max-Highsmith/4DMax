import os
from scipy.stats import pearsonr
import functools
import time
import matplotlib.pyplot as plt
import pdb
import torch
import numpy as np

np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

#lr        = .001
#struc_name = "struc2"
#struc_name  = "PSC_rep1_1"
#epochs     = 1000
#epochs     = 100
#res        = 100000
#lr         = .01

eta         = 1000
alpha       = 0.6
lr          = .0001
epochs      = 1000
res         = 50000
struc_name  = "PSC_rep1_1"

'''
def movement(struc_t):
	loss = 0
	T    = struc_t.shape[0]
	for i in range(0, T-1):
		next_st = struc_t[i+1]
		curr_st = struc_t[i]
		loss += np.linalg.norm(next_st-curr_st)
	return loss
'''

def movement(struc_t):
	loss = np.linalg.norm(struc_t[0:-1]-struc_t[1:])**2
	return loss

'''
def movementLoss(struc_t):
	start_time = time.time()
	change = np.zeros(struc_t.shape)
	T = struc_t.shape[0]
	I = struc_t.shape[1]
	C = struc_t.shape[2]
	for t in range(0,T-1):
		for i in range(0,I):
			denom = 0
			for c in range(0,C):
				denom += (struc_t[t,i,c] - struc_t[t+1,i,c])**2
			denom = np.sqrt(denom)
			for c in range(0,C):
				num = struc_t[t,i,c] - struc_t[t+1,i,c]
				change[t,i,c] = num/denom
	print("movementLoss", )
	return change
'''

def movementLoss(struc_t):
	start = time.time()
	change = np.zeros(struc_t.shape)
	change[0:-1]  = struc_t[0:-1]-struc_t[1:]
	print("moveloss:",time.time()-start)
	return change
	
def pcc_distance(hic_dist, wish_dist):
	#al = np.corrcoef(hic_dist, wish_dist)	
	val = pearsonr(hic_dist, wish_dist)
	print(val)

def pcc_distances(hic_dists, struc_t, row_tau, col_tau):
	val = {}
	wish_dists = getWishDistances(struc_t, row_tau, col_tau)
	for t in hic_dists.keys():
		val[t] = pearsonr(hic_dists[t], wish_dists[t])
	print(val)

def show_struc(structure, t, struc_name, window):
	print("saving "+str(t))
	plt.close()
	plt.clf()
	fig    = plt.figure()
	ax     = plt.axes(projection="3d")
	x      = structure[:,0]
	y      = structure[:,1]
	z      = structure[:,2]
	ax.plot(x,y,z, linewidth=1)
	ax.scatter(x[0],y[0],z[0], c="red")
	ax.scatter(x[10],y[10],z[10], c="blue")
	ax.scatter(x[4],y[4],z[4], c="green")
	ax.scatter(x[6],y[6],z[6], c="orange")
	ax.set_xlim(window[0], window[1])
	ax.set_ylim(window[0], window[1])
	ax.set_zlim(window[0], window[1])
	ax.set_title('{:.2f}'.format(ts[t]))
	for i in range(0,1):
		ax.text(x[i],y[i],z[i], str(i))
	for i in range(x.shape[0]-1,x.shape[0]):
		ax.text(x[i],y[i],z[i], str(i))
	plt.savefig("Image_Results/"+struc_name+"/treason_"+str(t)+".png")

def struc2contacts(struc):
	mat = np.zeros((struc.shape[0], struc.shape[0]))
	for i in range(0, mat.shape[0]):
		for j in range(0, mat.shape[1]):
			distance = np.linalg.norm(struc[i]-struc[j])
			if distance == 0:
				mat[i,j] =0
			else:
				mat[i,j] = 1/distance
				mat[j,i] = 1/distance
	big = np.max(mat)*1.5
	for i in range(0, mat.shape[0]):
		mat[i,i] = big
	return mat

def saveContacts(struc_t):
	np.save("Generated_Structures/"+struc_name, struc_t)
	for t in range(0, struc_t.shape[0]):
		mat = struc2contacts(struc_t[t])
		out = open("Generated_Contact_Maps/"+struc_name+"/"+str(t)+".txt", 'w')
		for i in range(0, mat.shape[0]):
			for j in range(i+1, mat.shape[0]):
				out.write(str(i*res)+"\t"+str(j*res)+"\t"+str(mat[i,j])+"\n")
		

def if2dist(contact_maps):
	#alpha = 1
	return 1/(contact_maps**alpha)

def getWishDistances(struc_t, row_tau, col_tau):
	wishes = {}
	for tau in range(0, len(row_tau.keys())):
		t = np.argwhere(ts==tau)[0][0]
		wishes[tau] = getWishDist(struc_t[t], row_tau[tau], col_tau[tau])
	return wishes

def getWishDist(struc, row, col):
	start = time.time()
	wish  = np.zeros(row.shape)
	wish  = np.linalg.norm(struc[row]-struc[col],axis=1)
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


taos = np.array([0,1,2,3,4,5])
ts   = np.linspace(0,5,21)
#taos = np.array([0,1,5])
#ts    =np.array([0,1.,2.,3.,4.,5.])
#three D structure
map_tao       = {} 
row_tao       = {}
col_tao       = {}
hic_dist_tao  = {}
ifs_tao       = {}
n_tao         = {}
n_min_tao     = {}

fn=['day_B_rep_1_chro_18', 
    'day_D2_rep_1_chro_18',
    'day_D4_rep_1_chro_18',
    'day_D6_rep_1_chro_18',
    'day_D8_rep_1_chro_18',
    'day_ES_rep_1_chro_18']
for tao in taos:
	#map_tao[tao]         = np.loadtxt("Synthetic_Data/Synthetic_Contact_Maps/"+struc_name+"_"+str(tao)+".txt")
	#map_tao[tao]         = np.loadtxt("Real Data/chr9_100000.txt")
	map_tao[tao]          = np.loadtxt("Real_Data/iPluripotent/"+str(fn[tao]))
	#map_tao[tao]          = np.loadtxt("Real_Data/iPluripotent/day_D2_rep_1_chro_18")
	row_tao[tao]          = (map_tao[tao][:,0].astype(int)/res).astype(int)
	col_tao[tao]          = (map_tao[tao][:,1].astype(int)/res).astype(int)
	ifs_tao[tao]          = map_tao[tao][:,2]
	hic_dist_tao[tao]     = if2dist(ifs_tao[tao])
	n_tao[tao]            = np.max((row_tao[tao],col_tao[tao]))
	n_min_tao[tao]        = np.min((row_tao[tao],col_tao[tao]))

n_max  = n_tao[list(n_tao.keys())[0]]
n_min  = n_min_tao[list(n_tao.keys())[0]]

for tao in taos:
	row_tao[tao] = row_tao[tao] - n_min_tao[tao]
	col_tao[tao] = col_tao[tao] - n_min_tao[tao]

np.random.seed(0)
struc_t       = np.random.rand(ts.shape[0], n_max+1-n_min, 3)


def getLikeChange(hic_dist_tao, row_tao, col_tao, struc_t, changea, changeb, t, struc_index):
	start = time.time()
	dl_ddk, ddk_dxyz = getGradient(hic_dist_tao[t],
					row_tao[t],
					col_tao[t],
					struc_t[struc_index])
	#print("getGradient:", time.time()-start)
	start = time.time()
	grada =  (ddk_dxyz.transpose()*dl_ddk).transpose()
	gradb = -(ddk_dxyz.transpose()*dl_ddk).transpose()
	changea = np.zeros(struc_t[struc_index].shape)
	changeb = np.zeros(struc_t[struc_index].shape)
	for i in range(0,3):
		changea[:,i] = np.bincount(row_tao[t],
				weights=grada[:,i],
				minlength=n_max-n_min+1)

		changeb[:,i] = np.bincount(col_tao[t],
				weights=gradb[:,i],
				minlength=n_max-n_min+1)

	#print("likeChange:", time.time()-start)
	return changea, changeb

def likelihoodloss(hic_dist_tao, row_tao, col_tao, struc_t):
	start = time.time()
	change  = np.zeros(struc_t.shape)
	changea = np.zeros(struc_t.shape)
	changeb = np.zeros(struc_t.shape)
	for t in ts:
		if float(t) in taos:
			struc_index = np.where(ts==t)[0][0]
			changea[struc_index], changeb[struc_index] = getLikeChange(hic_dist_tao,
				 		row_tao,
						col_tao,
						struc_t,
						changea,
						changeb,
						t,
						struc_index)
		else:
			struc_index = np.where(ts==t)[0][0]
			lower = taos[taos -t<0]
			upper = taos[taos -t>0]
			a1    = lower[np.argmin(np.abs(lower-t))]
			a2    = upper[np.argmin(np.abs(upper-t))]
			w2    = (t-a1)/np.abs(a1-a2)
			w1    = (a2-t)/np.abs(a1-a2)
			#print(a1,a2,w1,w2)
			changea1, changeb1 = getLikeChange(hic_dist_tao,
							row_tao,
							col_tao,
							struc_t,
							changea,
							changeb,
							a1,
							struc_index)

			changea2, changeb2 = getLikeChange(hic_dist_tao,
							row_tao,
							col_tao,
							struc_t,
							changea,
							changeb,
							a2,
							struc_index)
			changea[struc_index] += w1*changea1+w2*changea2
			changeb[struc_index] += w1*changeb1+w2*changeb2
	change = changea+changeb
	print("likelihoodloss", time.time()-start)
	return -change

#eta =3
#eta =10
for e in range(0, epochs):
	print(e)
	#start = time.time()
	likelihood_loss  = likelihoodloss(hic_dist_tao, row_tao, col_tao, struc_t)
	#print("likelihood_loss",time.time()- start)
	#start = time.time()
	movement_loss    = movementLoss(struc_t)
	#print("likelihood_loss",time.time()- start)
	print("movement: ", movement(struc_t))
	struc_t -= lr*(likelihood_loss+(eta*movement_loss))

	#loss
	pcc_distances(hic_dist_tao, struc_t, row_tao, col_tao)

for t in range(0, struc_t.shape[0]):
	window = (np.min(struc_t[:,:], axis=(0,1,2)), np.max(struc_t[:,:], axis=(0,1,2)))
	
	show_struc(struc_t[t],t, struc_name, window)

saveContacts(struc_t)
print(ts)
os.system("./make_gif.sh "+str(ts.shape[0]-1))
