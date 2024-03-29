import pdb
from scipy.stats import pearsonr
import time
import numpy as np
import cupy as cp
import matplotlib.pyplot as plt


def loadStrucAtTimeAsMat(struc, t):
	struc = np.load(struc)
	mat_struc = struc2contacts(struc[t])
	return mat_struc

def loadConstraintAsMat(stri, res=50000):
	contact_map = np.loadtxt(stri)
	rows = contact_map[:,0]
	cols = contact_map[:,1]
	vals = contact_map[:,2]
	rows = (rows/res).astype(int)
	cols = (cols/res).astype(int)
	mat  = constraints2mats(rows, cols, vals)
	return mat

def pcc_distance(hic_dist, wish_dist):
        val = pearsonr(hic_dist, wish_dist)
        print(val)

def pcc_distances(hic_dists, struc_t, row_tau, col_tau, ts):
        val = {}
        wish_dists = getWishDistances(struc_t, row_tau, col_tau,ts)
        for t in hic_dists.keys():
                val[t] = pearsonr(hic_dists[t], wish_dists[t])
        return val

def pcc_distanceGPU(hic_dist, wish_dist):
        val = pearsonr(hic_dist, wish_dist)
        print(val)

def pcc_distancesGPU(hic_dists, struc_t, row_tau, col_tau, ts):
        #ts      = cp.asnumpy(ts)
        #struc_t = cp.asnumpy(struc_t)
        val = {}
        wish_dists = getWishDistancesGPU(struc_t, row_tau, col_tau,ts)
        for t in hic_dists.keys():
                val[t] = pearsonr(cp.asnumpy(hic_dists[t]), cp.asnumpy(wish_dists[t]))
        return val

def constraints2mats(row, col, ifs):
	bigbin   = np.max((row,col))
	smallbin = np.min((row,col))
	mat = np.zeros((bigbin-smallbin+1, bigbin-smallbin+1))
	for r,c,i in zip(row, col, ifs):
		mat[r-smallbin,c-smallbin] = i
		mat[c-smallbin,r-smallbin] = i
	return mat

def show_struc_indiv(structure):
        plt.close()
        plt.clf()
        fig    = plt.figure()
        ax     = plt.axes(projection="3d")
        x      = structure[:,0]
        y      = structure[:,1]
        z      = structure[:,2]
        ax.plot(x,y,z, linewidth=1)
        plt.show()



def show_struc(structure, t, struc_name, window, ts):
        print("saving "+str(t))
        plt.close()
        plt.clf()
        fig    = plt.figure()
        ax     = plt.axes(projection="3d")
        x      = structure[:,0]
        y      = structure[:,1]
        z      = structure[:,2]
        ax.plot(x,y,z, linewidth=1)
        ax.scatter(x[0],y[0],z[0], c="red")
        ax.scatter(x[10],y[10],z[10], c="blue")
        ax.scatter(x[4],y[4],z[4], c="green")
        ax.scatter(x[6],y[6],z[6], c="orange")
        ax.set_xlim(window[0], window[1])
        ax.set_ylim(window[0], window[1])
        ax.set_zlim(window[0], window[1])
        ax.set_title('{:.2f}'.format(ts[t]))
        for i in range(0,1):
                ax.text(x[i],y[i],z[i], str(i))
        for i in range(x.shape[0]-1,x.shape[0]):
                ax.text(x[i],y[i],z[i], str(i))
        plt.savefig("Image_Results/"+struc_name+"/treason_"+str(t)+".png")

def struc2contacts(struc):
        mat = np.zeros((struc.shape[0], struc.shape[0]))
        for i in range(0, mat.shape[0]):
                for j in range(0, mat.shape[1]):
                        distance = np.linalg.norm(struc[i]-struc[j])
                        if distance == 0:
                                mat[i,j] =0
                        else:
                                mat[i,j] = 1/distance
                                mat[j,i] = 1/distance
        big = np.max(mat)*1.5
        for i in range(0, mat.shape[0]):
                mat[i,i] = big
        return mat

def saveStruc(struc_t, ARGS):
	np.save(struc_name, struc_t)

def saveContacts(struc_t, struc_name, res):
        np.save("Generated_Structures/"+struc_name, struc_t)
        for t in range(0, struc_t.shape[0]):
                mat = struc2contacts(struc_t[t])
                out = open("Generated_Contact_Maps/"+struc_name+"/"+str(t)+".txt", 'w')
                for i in range(0, mat.shape[0]):
                        for j in range(i+1, mat.shape[0]):
                                out.write(str(i*res)+"\t"+str(j*res)+"\t"+str(mat[i,j])+"\n")



def if2dist(contact_maps, alpha):
	val= 1/(contact_maps**alpha)
	#if np.isinf(val).any():
	#	val[np.where(np.isinf(val))] = np.max(val[np.logical_not(np.isinf(val))])
	return val

def getWishDistances(struc_t, row_tau, col_tau, ts):
        wishes = {}
        #for tau in range(0, len(row_tau.keys())):
        for tau in list(row_tau.keys()):
                t = np.argwhere(ts==tau)[0][0]
                wishes[tau] = getWishDist(struc_t[t], row_tau[tau], col_tau[tau])
        return wishes

def getWishDistancesGPU(struc_t, row_tau, col_tau, ts):
        wishes = {}
        #for tau in range(0, len(row_tau.keys())):
        for tau in list(row_tau.keys()):
                t = np.argwhere(cp.asnumpy(ts)==tau)[0][0]
                wishes[tau] = getWishDistGPU(struc_t[t], row_tau[tau], col_tau[tau])
        return wishes

def getWishDistGPU(struc, row, col):
	wish = cp.zeros(row.shape)
	wish = cp.linalg.norm(struc[row]-struc[col], axis=1)
	return wish

def getWishDist(struc, row, col):
        wish  = np.zeros(row.shape)
        wish  = np.linalg.norm(struc[row]-struc[col],axis=1)
        return wish

