import pdb
import numpy as np
import json
import sys

out_name = sys.argv[1]
step     = int(sys.argv[2])
chro     = sys.argv[3]
rep      = int(sys.argv[4])
res      = 500000
start_t  = 0
end_t    = 10

name     = "ipsc_small"
taos     = np.array([0,2,4,6,8,10])

dataset = ["Real_Data/iPluripotent/revised/day_Ba_rep_"+str(rep)+"_chro_"+str(chro),
	"Real_Data/iPluripotent/revised/day_D2_rep_"+str(rep)+"_chro_"+str(chro),
	"Real_Data/iPluripotent/revised/day_D4_rep_"+str(rep)+"_chro_"+str(chro),
	"Real_Data/iPluripotent/revised/day_D6_rep_"+str(rep)+"_chro_"+str(chro),
	"Real_Data/iPluripotent/revised/day_D8_rep_"+str(rep)+"_chro_"+str(chro),
	"Real_Data/iPluripotent/revised/day_ES_rep_"+str(rep)+"_chro_"+str(chro),
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
