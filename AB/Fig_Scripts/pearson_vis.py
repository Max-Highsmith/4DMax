import pdb
import numpy as np
import matplotlib.pyplot as plt


#chros = list(range(1,6))
#chros = list(range(6,11))
#chros = list(range(11,16))
chros = list(range(16,20))
days  = ['B','D2','D4','D6','D8','ES']

for day in days:
	fig, ax = plt.subplots(len(chros),2, figsize=(3,10))
	for c, chro in enumerate(chros):
		stria = "Pearson/real_chro_"+str(chro)+"_day_"+str(day)+"_missing_2_time_4.npy"
		strib = "Pearson/struc_chro_"+str(chro)+"_day_"+str(day)+"_missing_6_time_12.npy"
		peara = np.load(stria)
		pearb = np.load(strib)
		ax[c,0].imshow(np.clip(peara,-1,1), cmap='RdBu')
		ax[c,1].imshow(np.clip(pearb,-1,1), cmap='RdBu')
		ax[c,0].set_yticks([])
		ax[c,0].set_xticks([])
		ax[c,1].set_yticks([])
		ax[c,1].set_xticks([])
		ax[c,0].set_ylabel("Chro"+str(chro))
		ax[c,0].set_xlabel("Real")
		ax[c,1].set_xlabel("Interp")
	fig.suptitle("Day "+str(day))
	plt.savefig("Figs/Pearson/pearson_day_"+str(day)+"_chro_"+str(chros[0]))
	plt.close()
