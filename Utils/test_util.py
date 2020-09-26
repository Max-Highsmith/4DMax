import time
import pdb
import numpy as np
import cupy  as cp
import pytest
import util as ut


def test_getWishDistances():
	struc           = np.load("Utils/test_data/test_struc_getWishDistances.npy")
	row_tau         = np.load("Utils/test_data/test_row_tau_getWishDistances.npy", allow_pickle=True).item()
	col_tau         = np.load("Utils/test_data/test_col_tau_getWishDistances.npy", allow_pickle=True).item()
	ts              = np.load("Utils/test_data/test_ts_getWishDistances.npy")
	real_wishes     = np.load("Utils/test_data/test_getWishDistances.npy", allow_pickle=True).item()
	start_time      = time.time()
	passed_wishes   = ut.getWishDistances(struc, row_tau, col_tau, ts)
	print("getWishDistances", time.time() - start_time)
	for k in list(passed_wishes.keys()):
		assert((real_wishes[k] == passed_wishes[k]).all())



def test_getWishDistancesGPU():
	struc           = cp.load("Utils/test_data/test_struc_getWishDistances.npy")
	row_tau         = np.load("Utils/test_data/test_row_tau_getWishDistances.npy", allow_pickle=True).item()
	col_tau         = np.load("Utils/test_data/test_col_tau_getWishDistances.npy", allow_pickle=True).item()
	for i in row_tau.keys():
		row_tau[i] = cp.array(row_tau[i])
		col_tau[i] = cp.array(col_tau[i])

	ts              = cp.load("Utils/test_data/test_ts_getWishDistances.npy")
	real_wishes     = np.load("Utils/test_data/test_getWishDistances.npy", allow_pickle=True).item()
	for i in real_wishes.keys():
		real_wishes[i] = cp.array(real_wishes[i])
	start_time      = time.time()
	passed_wishes   = ut.getWishDistancesGPU(struc, row_tau, col_tau, ts)
	print("getWishDistancesGPU", time.time() - start_time)
	for k in list(passed_wishes.keys()):
		assert(((real_wishes[k] - passed_wishes[k]) < 1e-9).all())


def test_getWishDist():
	struc     = np.load("Utils/test_data/test_struc.npy")
	row       = np.load("Utils/test_data/test_row.npy")
	col       = np.load("Utils/test_data/test_col.npy")
	real_wish = np.load("Utils/test_data/test_wish.npy")
	start_t    = time.time()
	wish      = ut.getWishDist(struc, row, col)
	print("\ngetWishDist",str(time.time() - start_t),"\n")
	assert((wish == real_wish).all())

def test_getWishDistGPU():
	struc     = cp.load("Utils/test_data/test_struc.npy")
	row       = cp.load("Utils/test_data/test_row.npy")
	col       = cp.load("Utils/test_data/test_col.npy")
	real_wish = cp.load("Utils/test_data/test_wish.npy")
	start_t   = time.time()
	wish      = ut.getWishDistGPU(struc, row, col)
	print("\ngetWishDistGPU",str(time.time() - start_t),"\n")
	assert(((wish - real_wish) <1e-10).all())

def test_pcc_distances():
	hic_dist_tao = np.load("Utils/test_data/test_hic_dist_pcc.npy", allow_pickle=True).item()
	struc_t      = np.load("Utils/test_data/test_struc_pcc.npy")
	row_tau      = np.load("Utils/test_data/test_row_pcc.npy", allow_pickle=True).item()
	col_tau      = np.load("Utils/test_data/test_col_pcc.npy", allow_pickle=True).item()
	ts           = np.load("Utils/test_data/test_ts_pcc.npy")
	real_val     = np.load("Utils/test_data/test_vals_pcc.npy",allow_pickle=True).item()
	start_time   = time.time()
	passed_val = ut.pcc_distances(hic_dist_tao, struc_t, row_tau, col_tau, ts)
	print("pcc_distances", str(time.time() - start_time))
	print("pcc")
	assert((passed_val ==real_val))

def test_pcc_distancesGPU():
	hic_dist_tao = np.load("Utils/test_data/test_hic_dist_pcc.npy", allow_pickle=True).item()
	for k in hic_dist_tao.keys():
		hic_dist_tao[k] = cp.array(hic_dist_tao[k])
	struc_t      = cp.load("Utils/test_data/test_struc_pcc.npy")
	row_tau      = np.load("Utils/test_data/test_row_pcc.npy", allow_pickle=True).item()
	col_tau      = np.load("Utils/test_data/test_col_pcc.npy", allow_pickle=True).item()
	for i in row_tau.keys():
		row_tau[i] = cp.array(row_tau[i])
		col_tau[i] = cp.array(col_tau[i])

	ts           = cp.load("Utils/test_data/test_ts_pcc.npy")
	real_val     = np.load("Utils/test_data/test_vals_pcc.npy",allow_pickle=True).item()
	#for k in real_val.keys():
	#	real_val[k] = cp.array(real_val[k])
	start_time = time.time()
	passed_val = ut.pcc_distancesGPU(hic_dist_tao, struc_t, row_tau, col_tau, ts)
	print("pcc_distancesGPU", str(time.time()-start_time))
	for k in passed_val.keys():	
		assert(((np.array(passed_val[k]) - np.array(real_val[k]))<1e-9).all())
	
