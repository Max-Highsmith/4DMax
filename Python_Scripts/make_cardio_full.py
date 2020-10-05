import pdb
import numpy as np
import json
import sys
from Utils import util as ut

out_name = sys.argv[1]
rep      = int(sys.argv[2])
step     = sys.argv[3]
res      = 1 #the res is really 500000 but the files store bins by increasing number 1
start_t  = 0
end_t    = 14
step     = 15

chro     = "all"
name     = "cardio_full"
taos     = np.array([0,2,5,14])

if rep == 1:
	dataset = ["Real_Data/Cardiomyocyte/RUES2/GSM2845448_ESC_Rep1_500KB_ICED.matrix",
		"Real_Data/Cardiomyocyte/RUES2/GSM2845450_MES_Rep1_500KB_ICED.matrix",
		"Real_Data/Cardiomyocyte/RUES2/GSM2845452_CP_Rep1_500KB_ICED.matrix",
		"Real_Data/Cardiomyocyte/RUES2/GSM2845454_CM_Rep1_500KB_ICED.matrix"]
if rep == 2:
	dataset = ["Real_Data/Cardiomyocyte/RUES2/GSM2845449_ESC_Rep2_500KB_ICED.matrix",
		"Real_Data/Cardiomyocyte/RUES2/GSM2845451_MES_Rep2_500KB_ICED.matrix",
		"Real_Data/Cardiomyocyte/RUES2/GSM2845453_CP_Rep2_500KB_ICED.matrix",
		"Real_Data/Cardiomyocyte/RUES2/GSM2845455_CM_Rep2_500KB_ICED.matrix"]

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
