import pdb
import numpy as np
import json
import sys
from Utils import util as ut

out_name = sys.argv[1]
rep      = int(sys.argv[2])

res      = 100000
start_t  = 0
end_t    = 5
step     = 21

chro     = "all"
name     = "synthetic_full"
taos     = np.array([0,1,2,3,4,5])

dataset = ["Synthetic_Data/Synthetic_Contact_Maps/struc"+str(rep)+"_0.txt",
	"Synthetic_Data/Synthetic_Contact_Maps/struc"+str(rep)+"_1.txt",
	"Synthetic_Data/Synthetic_Contact_Maps/struc"+str(rep)+"_2.txt",
	"Synthetic_Data/Synthetic_Contact_Maps/struc"+str(rep)+"_3.txt",
	"Synthetic_Data/Synthetic_Contact_Maps/struc"+str(rep)+"_4.txt",
	"Synthetic_Data/Synthetic_Contact_Maps/struc"+str(rep)+"_5.txt"]

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
