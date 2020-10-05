from scipy.stats import spearmanr
from scipy.stats import pearsonr
import numpy as np
import matplotlib.pyplot as plt
import pdb



def getStrucDistVec(struc):
	distvec = []
	for i in range(0, struc.shape[0]):
		for j in range(i, min((i+100),struc.shape[0])):#struc.shape[0]):
			dist = np.linalg.norm(struc[i]-struc[j])
			distvec.append(dist)
	return np.array(distvec)

def compare3D(struca, strucb):
	dista =	getStrucDistVec(struca)
	distb =	getStrucDistVec(strucb)
	pear  = pearsonr(dista, distb)[0]
	spear = spearmanr(dista, distb)[0]
	return pear, spear

def compare4D(struca, strucb):
	pears  = []
	spears = []
	for t, time in enumerate(range(0,struca.shape[0])):
		dv_a = getStrucDistVec(struca[t])
		dv_b = getStrucDistVec(strucb[t])
		pears.append(pearsonr(dv_a, dv_b)[0])
		spears.append(spearmanr(dv_a, dv_b)[0])
	spear_context = spearmanr(getStrucDistVec(strucb[0]), getStrucDistVec(strucb[strucb.shape[0]-1]))
	pear_context = pearsonr(getStrucDistVec(strucb[0]), getStrucDistVec(strucb[strucb.shape[0]-1]))
	return (np.mean(spears), np.mean(pears)), (spear_context, pear_context)

		
def compare4D_Diff_gran(struca, strucb, start, end):
	start = 0
	end   = 14
	grana = struca.shape[0]
	granb = strucb.shape[0]

	if grana > granb:
		print("switching")
		temp   = struca
		struca = strucb
		strucb = temp
		temp   = grana
		grana  = granb
		granb  = temp

	days_a = np.linspace(start, end, grana)
	days_b = np.linspace(start, end, granb)

	spears = []
	pears  = []
	for d, day in enumerate(days_a):
		indx = np.argwhere(days_b==day)[0][0]
		dv_a = getStrucDistVec(struca[d])
		dv_b = getStrucDistVec(strucb[indx])
		spears.append(spearmanr(dv_a, dv_b)[0])
		pears.append(pearsonr(dv_a, dv_b)[0])
	return spears, pears
	
	
