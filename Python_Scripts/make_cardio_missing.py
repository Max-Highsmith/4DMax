import pdb
import numpy as np
import json
import sys
from Utils import util as ut

out_name = sys.argv[1]
rep      = int(sys.argv[2])
chro     = sys.argv[3]
missing  = int(sys.argv[4])

res      = 1 #the res is really 500000 but the files store bins by increasing number 1
start_t  = 0
end_t    = 14
step     = 15

name     = "cardio_missing_"+str(missing)
taos     = np.array([0,2,5,14])

if rep == 1:
	dataset = ["Real_Data/Cardiomyocyte/RUES2/By_Chros/GSM2845448_ESC_Rep1_500KB_"+str(chro),
		"Real_Data/Cardiomyocyte/RUES2/By_Chros/GSM2845450_MES_Rep1_500KB_"+str(chro),
		"Real_Data/Cardiomyocyte/RUES2/By_Chros/GSM2845452_CP_Rep1_500KB_"+str(chro),
		"Real_Data/Cardiomyocyte/RUES2/By_Chros/GSM2845454_CM_Rep1_500KB_"+str(chro)]
if rep == 2:
	dataset = ["Real_Data/Cardiomyocyte/RUES2/By_Chros/GSM2845449_ESC_Rep2_500KB_"+str(chro),
		"Real_Data/Cardiomyocyte/RUES2/By_Chros/GSM2845451_MES_Rep2_500KB_"+str(chro),
		"Real_Data/Cardiomyocyte/RUES2/By_Chros/GSM2845453_CP_Rep2_500KB_"+str(chro),
		"Real_Data/Cardiomyocyte/RUES2/By_Chros/GSM2845455_CM_Rep2_500KB_"+str(chro)]

indx = np.where(taos==int(missing))[0][0]

taos    = np.delete(taos, indx)
dataset = np.delete(dataset, indx)

dd = {"name":name,
	"step":step,
	"res":res,
	"chro":chro,
	"rep":rep,
	"start_t": start_t,
	"end_t": end_t,
	"taos":taos.tolist(),
	"dataset": dataset.tolist()}

with open(out_name, 'w') as fp:
	json.dump(dd, fp)
