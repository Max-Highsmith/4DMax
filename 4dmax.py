import cupy as cp
import json
import sys
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

#settings
np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
np.random.seed(0)

dataset_fn = sys.argv[1]
hyper_fn   = sys.argv[2]

#Hyper Parameters
param_set  = open(hyper_fn)
param_vals = json.load(param_set)
eta        = int(param_vals['eta'])
alpha      = float( param_vals['alpha'])
lr         = float(param_vals['lr'])
epochs     = int(param_vals['epoch'])

#Dataset
dataset     = open(dataset_fn)
data_vals  = json.load(dataset)
struc_name = data_vals['name']
res        = data_vals['res']
rep        = data_vals['rep']
fn         = data_vals['dataset']
start_t    = data_vals['start_t']
end_t      = data_vals['end_t']
chro       = data_vals['chro']
step       = int(data_vals['step'])
taos       = np.array(data_vals['taos'])

ts   = np.linspace(start_t,end_t,step)


#three D structure
map_tao       = {} 
row_tao       = {}
col_tao       = {}
hic_dist_tao  = {}
ifs_tao       = {}
n_tao         = {}
n_min_tao     = {}

#load data and build starting strucs
for s, tao in enumerate(taos):
	#map_tao[tao]         = np.loadtxt("Synthetic_Data/Synthetic_Contact_Maps/"+struc_name+"_"+str(tao)+".txt")
	map_tao[tao]          = np.loadtxt(str(fn[s]))
	row_tao[tao]          = (map_tao[tao][:,0].astype(int)/res).astype(int)
	col_tao[tao]          = (map_tao[tao][:,1].astype(int)/res).astype(int)
	ifs_tao[tao]          = map_tao[tao][:,2]
	hic_dist_tao[tao]     = ut.if2dist(ifs_tao[tao], alpha)
	n_tao[tao]            = np.max((row_tao[tao],col_tao[tao]))
	n_min_tao[tao]        = np.min((row_tao[tao],col_tao[tao]))

n_max  = n_tao[list(n_tao.keys())[0]]
#n_min  = n_min_tao[list(n_tao.keys())[0]]
###NEW MAX
n_max   = np.max(list(n_tao.values()))
###
n_min   = np.min(list(n_min_tao.values()))
for s, tao in enumerate(taos):
	row_tao[tao] = row_tao[tao] - n_min_tao[tao]
	col_tao[tao] = col_tao[tao] - n_min_tao[tao]
struc_t       = np.random.rand(ts.shape[0], n_max+1-n_min, 3)

GPU = True
if GPU:
	print("Using GPU")
	for i in hic_dist_tao.keys():
		hic_dist_tao[i] = cp.array(hic_dist_tao[i])
	struc_t         = cp.array(struc_t)	
	ts              = cp.array(ts)
	taos            = cp.array(taos)

	pcc_log     = []
	mov_log     = []
	full_time   = []
	for e in range(0, epochs):
		start_time = time.time()
		likelihood_loss  = li.likelihoodlossGPU(hic_dist_tao, row_tao, col_tao, struc_t, ts, taos, n_max, n_min)
		movement_loss    = mv.movementLossGPU(struc_t)
		print(e, "movement: ", mv.movementGPU(struc_t))
		struc_t -= lr*(likelihood_loss+(eta*movement_loss))

		#loss
		pc_dist  = ut.pcc_distancesGPU(hic_dist_tao, struc_t, row_tao, col_tao, ts)
		print(e, "pc_dist", pc_dist)
		movement = mv.movementGPU(struc_t)
		pcc_log.append(pc_dist)
		mov_log.append(movement)
		full_time.append(time.time()- start_time)
		print("GPU epoch time:",str(time.time() - start_time))

	#save everthing
	save_str= ""+struc_name+"_rep_"+str(rep)+"_eta_"+str(eta)+"_alpha_"+str(alpha)+"_lr_"+str(lr)+"_epoch_"+str(epochs)+"_res_"+str(res)+"_step_"+str(step)+"_chro_"+str(chro)
	logg = {'pcc_log':pcc_log,
		'mov_log':mov_log,
		'time':full_time}
	np.save("Generated_Struc_Logs/"+save_str, logg)
	np.save("Generated_Structures/"+save_str, struc_t)
	os.system("./make_gif.sh "+str(ts.shape[0]-1))

else:
	#train
	pcc_log     = []
	mov_log     = []
	full_time   = []
	for e in range(0, epochs):
		pdb.set_trace()
		start_time = time.time()
		likelihood_loss  = li.likelihoodloss(hic_dist_tao, row_tao, col_tao, struc_t, ts, taos, n_max, n_min)
		movement_loss    = mv.movementLoss(struc_t)
		
		print(e, "movementt: ", mv.movement(struc_t))
		struc_t -= lr*(likelihood_loss+(eta*movement_loss))

		#loss
		pc_dist  = ut.pcc_distances(hic_dist_tao, struc_t, row_tao, col_tao, ts)
		print(e, "pcc_dist", pc_dist)
		movement = mv.movement(struc_t)
		pcc_log.append(pc_dist)
		mov_log.append(movement)
		full_time.append(time.time()- start_time)
		print("GPU epoch time:",str(time.time() - start_time))

	#save everthing
	save_str= ""+struc_name+"_rep_"+str(rep)+"_eta_"+str(eta)+"_alpha_"+str(alpha)+"_lr_"+str(lr)+"_epoch_"+str(epochs)+"_res_"+str(res)+"_step_"+str(step)+"_chro_"+str(chro)
	logg = {'pcc_log':pcc_log,
		'mov_log':mov_log,
		'time':full_time}
	np.save("Generated_Struc_Logs/"+save_str, logg)
	np.save("Generated_Structures/"+save_str, struc_t)
	os.system("./make_gif.sh "+str(ts.shape[0]-1))

