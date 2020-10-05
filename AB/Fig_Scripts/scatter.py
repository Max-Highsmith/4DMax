from scipy.stats import pearsonr 
import pdb
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

#TIME = 20
#day     = 'D2'
#daytime =  2
days     = ['B','D2','D4','D6','D8','ES']
times    = [ 4, 8,12, 16]
mistimes = [ 2, 4, 6, 8 ]

colors = ['black', 'lightcoral', 'brown', 'red', 'sandybrown', 'palegreen', 'chartreuse', 'yellow', 'gold', 'darkorange', 'darkgreen', 'lime', 'green', 'deepskyblue', 'steelblue', 'slategrey', 'navy', 'blueviolet', 'plum', 'darkorchid', 'magenta', 'pink']
chros = [1,2,3,4,5,6,7,8,9,10,11,12,13,15,16,18,19]
#fig, ax = plt.subplots(len(days), len(mistimes))
#plt.subplots_adjust(wspace=0, hspace=0)
for d, day in enumerate(days):
	for t, (time, mistime) in enumerate(zip(times, mistimes)):
		fig, ax = plt.subplots(1)#len(days), len(mistimes))
		plt.subplots_adjust(wspace=0, hspace=0)
		pear_tot = 0
		for chro in chros:
			#real  = np.load("AB_Vecs/real_ipsc_day_"+str(day)+"_rep_1_chro_"+str(chro)+".npy")
			#struc = np.load("AB_Vecs/struc_ipsc_missing_"+str(mistime)+"_rep_1_eta_1000_alpha_0.6_lr_0.0001_epoch_400_res_50000_step_21_chro_"+str(chro)+".npy")
			real   = np.load("AB_Vecs/real_day_"+str(day)+ "_missing_"+str(mistime)+"_time_"+str(time)+"_chro_"+str(chro)+".npy")
			struc  = np.load("AB_Vecs/struc_day_"+str(day)+"_missing_"+str(mistime)+"_time_"+str(time)+"_chro_"+str(chro)+".npy")
			#if real.shape[0] != struc.shape[0]:
			#	continue
			#pear_score = pearsonr(real, struc[time])[0]
			pear_score = pearsonr(real, struc)[0]
			print(str(chro)+":"+str(pear_score))
			if pear_score < 0:
				struc_vec = (-1) * struc
				pear_score = pear_score*-1
			else:
				struc_vec = struc
			pear_tot += pear_score
			#ax[d,t].scatter(real, struc_vec, s=1, c=colors[chro], label=str(chro)+" P="+str(pear_score))
			#ax[d,t].set_xticks([])
			#ax[d,t].set_yticks([])
		#ax[d,t].text(-20,14,s="{:.2f}".format(pear_tot/len(chros)))
			ax.scatter(real, struc_vec, s=1, c=colors[chro], label=str(chro)+" P="+str(pear_score))
			ax.set_xticks([])
			ax.set_yticks([])
			ax.spines['right'].set_position('center')
			ax.spines['top'].set_position('center')
		print("AVERAGE:",str(pear_tot/len(chros)))
		ax.text(0,0,s="PCC={:.2f}".format(pear_tot/len(chros)), fontsize=30)


		plt.savefig("Figs/Scatters/day_"+str(day)+"_missing_"+str(mistime)+".png")
		plt.show()

