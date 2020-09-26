import numpy as np
import matplotlib.pyplot as plt
import pdb 


prefixes = {1:[
'GSM2845448_ESC_Rep1_500KB',
'GSM2845450_MES_Rep1_500KB',
'GSM2845452_CP_Rep1_500KB',
'GSM2845454_CM_Rep1_500KB',
],
2:[
'GSM2845449_ESC_Rep2_500KB',
'GSM2845451_MES_Rep2_500KB',
'GSM2845453_CP_Rep2_500KB',
'GSM2845455_CM_Rep2_500KB',
]
}
reps = [1,2]
for rep in reps:
	for prefix in prefixes[rep]:
		graph    = np.loadtxt("Real_Data/Cardiomyocyte/RUES2/"+prefix+"_bins.bed", str)
		x        = np.loadtxt("Real_Data/Cardiomyocyte/RUES2/"+prefix+"_ICED.matrix")
		for chro in range(1,23):
			index    = graph[graph[:,0]==str(chro)][:,3].astype(int)
			inrows   = np.in1d(x[:,0], index)
			incols   = np.in1d(x[:,1], index)
			keep     = np.logical_and(inrows, incols)
			contacts = x[keep]
			out = open("Real_Data/Cardiomyocyte/RUES2/By_Chros/"+prefix+"_"+str(chro),'w')
			for a in range(0,contacts.shape[0]):
				out.write(str(contacts[a][0].astype(int))+"\t"+str(contacts[a][1].astype(int))+"\t"+str(contacts[a][2].astype(float))+"\n")
