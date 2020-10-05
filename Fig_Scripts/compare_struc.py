from Utils import util as ut
import itertools
import cupy as cp
import time
import numpy as np
from scipy.stats import spearmanr
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import pdb

def distanceVec(struc):
	times, beads, xyz = struc.shape
	distVec = {}
	for t in range(0, times):
		distVec[t] = []
		for a_bead in range(0, beads):
			for b_bead in range(a_bead, beads):
				distVec[t].append(np.linalg.norm( struc[t, a_bead] - struc[t, b_bead]))

def distanceVecIndiv(struc):
	beads, xyz = struc.shape
	distVec = []
	for a_bead in range(0, beads):
		for b_bead in range(a_bead, beads):
			distVec.append(np.linalg.norm(struc[a_bead] - struc[b_bead]))
	return distVec

def distanceVecIndivFast(struc):
	beads, xyz = struc.shape
	indis      = np.indices((beads, beads))
	def getVal(i,j):
		return np.linalg.norm(struc[i] - struc[j])
	getVVec = np.vectorize(getVal)
	distMat = getVVec(indis[0],indis[1])
	alt     = np.triu(distMat)[np.triu_indices(distMat.shape[0])]
	return alt

	

struc    = {}
distVecs = {}
#load strucs
missings = [2,4,6,8]
reps     = [1,2]
chros    = [15,16,17,18,19]
for chro in chros:
	for missing in [2,4,6,8]:
		for rep in [1,2]:
			print(str(missing), str(rep))
			struc[missing, rep]  = np.load("Generated_Structures/ipsc_missing_"+str(missing)+"_rep_"+str(rep)+"_eta_1000_alpha_0.6_lr_0.0001_epoch_400_res_50000_step_21_chro_"+str(chro)+".npy")
			#for t in [0,4,8,12,16,20]:
			#	distVecs[missing, rep, t] = distanceVecIndiv(struc[missing, rep][t])

#build simple full struc corellation
#This creates a confusion matrix between different 3D snapshots of 4D structures with missing data
def timeConfusion(t,chro, rep):
	plt.close()
	plt.clf()
	plt.cla()
	reps=[rep]
	combos = list(itertools.product(*[missings, reps]))
	confusion = np.zeros((len(combos), len(combos)))
	fig, ax = plt.subplots(1)
	for a, combo_a in enumerate(combos):
		for b, combo_b in enumerate(combos):
			mis_a, rep_a = combo_a
			mis_b, rep_b = combo_b
			confusion[a, b] = spearmanr(struc[mis_a, rep_a][t], struc[mis_b, rep_b][t], axis=None)[0]
	cooo = ax.imshow(confusion, cmap="Reds")
	for (j,i), label in np.ndenumerate(confusion):
		ax.text(i,j,"{0:0.3f}".format(confusion[i,j]), ha='center', va='center')
	ax.set_xticks(list(range(0, len(combos))))
	ax.set_xticklabels(missings)
	ax.set_yticks(list(range(0, len(combos))))
	ax.set_yticklabels(missings)
	ax.set_title("Confusion between Missing Maps "+str(chro)+" time "+str(t)+" rep "+str(rep_a))
	ax.set_xlabel("Missing Day")
	ax.set_ylabel("Missing Day")
	name_str="timeConfusion"+"_time_"+str(t)+"_chro_"+str(chro)+"_rep_"+str(rep)
	plt.savefig("Figures/"+name_str)
	fig.colorbar(cooo)
	return confusion

times = np.linspace(0,10,21)
def confusionByTime(mis, rep, chro):
	plt.close()
	plt.clf()
	plt.cla()
	confusion = np.zeros((len(times), len(times)))
	fig, ax = plt.subplots(1, figsize=(10,10))
	for ta in range(0, struc[mis,rep].shape[0]):
		for tb in range(0, struc[mis, rep].shape[0]):
			confusion[ta,tb] = spearmanr(struc[mis, rep][ta], struc[mis, rep][tb], axis=None)[0]
	cooo = ax.imshow(confusion, cmap="Blues")
	#for (j, i), label in np.ndenumerate(confusion):
	#	ax.text(i,j, "{0:0.3f}".format(confusion[i,j]), ha='center', va='center')
	ax.set_xticks(list(range(0,len(times))))
	ax.set_yticks(list(range(0,len(times))))
	ax.set_xticklabels(times)
	ax.set_yticklabels(times)
	ax.set_xlabel("Day")
	ax.set_ylabel("Day")
	ax.set_title("Similarity over Time Chromosome "+str(chro)+" missing_"+str(mis)+"rep_"+str(rep))
	fig.colorbar(cooo)
	name_str="confusionByTime_"+"_mis_"+str(mis)+"_chro_"+str(chro)+"_rep_"+str(rep)
	plt.savefig("Figures/"+name_str)
	return confusion
	
#confusion = timeConfusion(2,16,1)
#confusion = confusionByTime(2,2, 15)

for chro in chros:
	for mis in missings:
		for rep in reps:
			print(str(chro), str(mis), str(rep))
			confusionByTime(mis,rep,chro)
			for t, time in enumerate(times):
				timeConfusion(t, chro, rep)

#confusion = confusionByTime(8,1, 15)
#confusion = confusionByTime(8,2, 15)
#confusion = confusionByTime(2,1, 15)
'''
alt   = distanceVecIndivFast(struc[2,2][2])
print("alt", str(time.time() - start_time))
start_time = time.time()
mainn = distanceVecIndiv(struc[2,2][2])
print("main", str(time.time() - start_time))
'''
