import os
from scipy.stats import pearsonr
import functools
import time
import matplotlib.pyplot as plt
import pdb
import torch
import numpy as np
import Utils.util as ut
import Utils.movement as mv
import Utils.likelihood as li
np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

#Parameters
eta         = 1000
alpha       = 0.6
lr          = .0001
#epochs      = 1000
epochs      = 2
res         = 50000
struc_name  = "PSC_rep1_1"

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
	map_tao[tao]          = np.loadtxt("Real_Data/iPluripotent/"+str(fn[tao]))
	row_tao[tao]          = (map_tao[tao][:,0].astype(int)/res).astype(int)
	col_tao[tao]          = (map_tao[tao][:,1].astype(int)/res).astype(int)
	ifs_tao[tao]          = map_tao[tao][:,2]
	hic_dist_tao[tao]     = ut.if2dist(ifs_tao[tao], alpha)
	n_tao[tao]            = np.max((row_tao[tao],col_tao[tao]))
	n_min_tao[tao]        = np.min((row_tao[tao],col_tao[tao]))

n_max  = n_tao[list(n_tao.keys())[0]]
n_min  = n_min_tao[list(n_tao.keys())[0]]

for tao in taos:
	row_tao[tao] = row_tao[tao] - n_min_tao[tao]
	col_tao[tao] = col_tao[tao] - n_min_tao[tao]

np.random.seed(0)
struc_t       = np.random.rand(ts.shape[0], n_max+1-n_min, 3)

for e in range(0, epochs):
	likelihood_loss  = li.likelihoodloss(hic_dist_tao, row_tao, col_tao, struc_t, ts, taos, n_max, n_min)
	movement_loss    = mv.movementLoss(struc_t)
	print(e, "movement: ", mv.movement(struc_t))
	struc_t -= lr*(likelihood_loss+(eta*movement_loss))

	#loss
	ut.pcc_distances(hic_dist_tao, struc_t, row_tao, col_tao, ts)

for t in range(0, struc_t.shape[0]):
	window = (np.min(struc_t[:,:], axis=(0,1,2)), np.max(struc_t[:,:], axis=(0,1,2)))
	ut.show_struc(struc_t[t],t, struc_name, window, ts)

ut.saveContacts(struc_t, struc_name, res)
print(ts)
os.system("./make_gif.sh "+str(ts.shape[0]-1))
