import pdb
import numpy as np
import json
import sys

out_name = sys.argv[1]
rep      = sys.argv[2]
chro     = sys.argv[3]
res      = 50000
start_t  = 0
end_t    = 3
step     = 7

name     = "adipose_full"
taos     = np.array([0,1,3])

dataset = ["Real_Data/Adipose/Adipose_D0_rep_"+str(rep)+"_chro_"+str(chro),
	   "Real_Data/Adipose/Adipose_D1_rep_"+str(rep)+"_chro_"+str(chro),
	   "Real_Data/Adipose/Adipose_D3_rep_"+str(rep)+"_chro_"+str(chro)
	]

dd = {"name":name,
	"step":step,
	"res":res,
	"chro":chro,
	"rep":rep,
	"start_t": start_t,
	"end_t": end_t,
	"taos":taos.tolist(),
	"dataset": dataset}

with open(out_name, 'w') as fp:
	json.dump(dd, fp)
