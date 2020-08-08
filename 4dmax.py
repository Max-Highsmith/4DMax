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

#Parameters
struc_name = sys.argv[1]
eta        = int(sys.argv[2])
alpha      = float(sys.argv[3])
lr         = float(sys.argv[4])
epochs     = int(sys.argv[5])
res        = int(sys.argv[6])
step       = int(sys.argv[7])
chro       = int(sys.argv[8])
rep        = int(sys.argv[9])

if struc_name == "iPluripotent":
          fn          = ["Real_Data/iPluripotent/day_Ba_rep_"+str(rep)+"_chro_"+str(chro),
                "Real_Data/iPluripotent/day_D2_rep_"+str(rep)+"_chro_"+str(chro),
     	       	"Real_Data/iPluripotent/day_D4_rep_"+str(rep)+"_chro_"+str(chro),
                "Real_Data/iPluripotent/day_D6_rep_"+str(rep)+"_chro_"+str(chro),
                "Real_Data/iPluripotent/day_D8_rep_"+str(rep)+"_chro_"+str(chro),
                "Real_Data/iPluripotent/day_ES_rep_"+str(rep)+"_chro_"+str(chro)]

          taos = np.array([0,1,2,3,4,5])
          ts   = np.linspace(0,5,step)


#three D structure
map_tao       = {} 
row_tao       = {}
col_tao       = {}
hic_dist_tao  = {}
ifs_tao       = {}
n_tao         = {}
n_min_tao     = {}

#load data and build starting strucs
for tao in taos:
	#map_tao[tao]         = np.loadtxt("Synthetic_Data/Synthetic_Contact_Maps/"+struc_name+"_"+str(tao)+".txt")
	map_tao[tao]          = np.loadtxt(str(fn[tao]))
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
struc_t       = np.random.rand(ts.shape[0], n_max+1-n_min, 3)


#train
pcc_log     = []
mov_log     = []
for e in range(0, epochs):
	likelihood_loss  = li.likelihoodloss(hic_dist_tao, row_tao, col_tao, struc_t, ts, taos, n_max, n_min)
	movement_loss    = mv.movementLoss(struc_t)
	
	print(e, "movement: ", mv.movement(struc_t))
	struc_t -= lr*(likelihood_loss+(eta*movement_loss))

	#loss
	pc_dist  = ut.pcc_distances(hic_dist_tao, struc_t, row_tao, col_tao, ts)
	movement = mv.movement(struc_t)
	pcc_log.append(pc_dist)
	mov_log.append(movement)

#save everthing
save_str= ""+struc_name+"_rep_"+str(rep)+"_eta_"+str(eta)+"_alpha_"+str(alpha)+"_lr_"+str(lr)+"_epoch_"+str(epochs)+"_res_"+str(res)+"_step_"+str(step)+"_chro_"+str(chro)
logg = {'pcc_log':pcc_log,
	'mov_log':mov_log}
np.save("Generated_Struc_Logs/"+save_str, logg)
np.save("Generated_Structures/"+save_str, struc_t)
os.system("./make_gif.sh "+str(ts.shape[0]-1))
