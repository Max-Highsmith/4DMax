import time
import pdb
import numpy as np
import cupy  as cp
import pytest
import likelihood as li
import util as ut

def test_getGradient():
	print("test")
	hic_dist         = np.load("Utils/test_data/test_hic_dist.npy")
	row              = np.load("Utils/test_data/test_row.npy")
	col              = np.load("Utils/test_data/test_col.npy")
	struc            = np.load("Utils/test_data/test_struc.npy")
	true_dl_ddk      = np.load("Utils/test_data/test_dl_ddk.npy")
	true_ddk_dxyz    = np.load("Utils/test_data/test_ddk_dxyz.npy")
	start_time       = time.time()
	dl_ddk, ddk_dxyz = li.getGradient(hic_dist, row, col, struc)
	print("getGradient", str(time.time()-start_time))
	assert((dl_ddk    == true_dl_ddk).all())
	assert((ddk_dxyz  == true_ddk_dxyz).all())

def test_getGradientGPU():
	print("test")
	hic_dist         = cp.load("Utils/test_data/test_hic_dist.npy")
	row              = cp.load("Utils/test_data/test_row.npy")
	col              = cp.load("Utils/test_data/test_col.npy")
	struc            = cp.load("Utils/test_data/test_struc.npy")
	true_dl_ddk      = cp.load("Utils/test_data/test_dl_ddk.npy")
	true_ddk_dxyz    = cp.load("Utils/test_data/test_ddk_dxyz.npy")
	start_time       = time.time()
	dl_ddk, ddk_dxyz = li.getGradientGPU(hic_dist, row, col, struc)
	print("getGradientGPU", str(time.time()-start_time))
	assert(((dl_ddk - true_dl_ddk)<1e-9).all())
	assert(((ddk_dxyz  - true_ddk_dxyz)<1e-9).all())

def test_getLikeChangeGPU():
	hic_dist_tao      = np.load("Utils/test_data/test_hic_dist_tao.npy", allow_pickle=True).item()
	row_tao           = np.load("Utils/test_data/test_row_tao.npy", allow_pickle=True).item()
	col_tao           = np.load("Utils/test_data/test_col_tao.npy", allow_pickle=True).item()
	for i in hic_dist_tao.keys():
		hic_dist_tao[i] = cp.array(hic_dist_tao[i])
	#for i in row_tao.keys():
	#	row_tao[i] = cp.array(row_tao[i])
	#for i in hic_dist_tao.keys():
	#	col_tao[i] = cp.array(col_tao[i])
	
	struc_t           = cp.load("Utils/test_data/test_struc_t.npy", allow_pickle=True)
	changea           = cp.load("Utils/test_data/test_changea.npy", allow_pickle=True)
	changeb           = cp.load("Utils/test_data/test_changeb.npy", allow_pickle=True)
	t                 = cp.load("Utils/test_data/test_t.npy", allow_pickle=True).item()
	struc_index       = np.load("Utils/test_data/test_struc_index.npy", allow_pickle=True).item()
	n_max             = np.load("Utils/test_data/test_n_max.npy", allow_pickle=True).item()
	n_min             = np.load("Utils/test_data/test_n_min.npy", allow_pickle=True).item()
	real_out_changea  = cp.load("Utils/test_data/test_real_out_changea.npy", allow_pickle=True)
	real_out_changeb  = cp.load("Utils/test_data/test_real_out_changeb.npy", allow_pickle=True)
	#real_out_changea  = cp.asnumpy(real_out_changea)
	#real_out_changeb  = cp.asnumpy(real_out_changeb)
	start_time = time.time()
	new_a, new_b      = li.getLikeChangeGPU(hic_dist_tao,
			 row_tao,
			 col_tao,
			 struc_t,
			 changea,
			 changeb,
			 t,
			 struc_index,
			 n_max,
			 n_min)
	
	print("getLikeChangeGPU",str(time.time()-start_time))
	assert(((new_a  - real_out_changea)<1e-9).all())
	assert(((new_b  - real_out_changeb)<1e-9).all())



def test_getLikeChange():
	hic_dist_tao      = np.load("Utils/test_data/test_hic_dist_tao.npy", allow_pickle=True).item()
	row_tao           = np.load("Utils/test_data/test_row_tao.npy", allow_pickle=True).item()
	col_tao           = np.load("Utils/test_data/test_col_tao.npy", allow_pickle=True).item()
	struc_t           = np.load("Utils/test_data/test_struc_t.npy", allow_pickle=True)
	changea           = np.load("Utils/test_data/test_changea.npy", allow_pickle=True)
	changeb           = np.load("Utils/test_data/test_changeb.npy", allow_pickle=True)
	t                 = np.load("Utils/test_data/test_t.npy", allow_pickle=True).item()
	struc_index       = np.load("Utils/test_data/test_struc_index.npy", allow_pickle=True).item()
	n_max             = np.load("Utils/test_data/test_n_max.npy", allow_pickle=True).item()
	n_min             = np.load("Utils/test_data/test_n_min.npy", allow_pickle=True).item()
	real_out_changea  = np.load("Utils/test_data/test_real_out_changea.npy", allow_pickle=True)
	real_out_changeb  = np.load("Utils/test_data/test_real_out_changeb.npy", allow_pickle=True)
	start_time = time.time()
	new_a, new_b      = li.getLikeChange(hic_dist_tao,
			 row_tao,
			 col_tao,
			 struc_t,
			 changea,
			 changeb,
			 t,
			 struc_index,
			 n_max,
			 n_min)
	
	print("getLikeChange",str(time.time()-start_time))
	assert(((new_a  - real_out_changea)<1e-9).all())
	assert(((new_b  - real_out_changeb)<1e-9).all())


def test_likelihoodloss():
	hic_dist_tao      = np.load("Utils/test_data/test_hic_dist_tao.npy", allow_pickle=True).item()
	row_tao           = np.load("Utils/test_data/test_row_tao.npy", allow_pickle=True).item()
	col_tao           = np.load("Utils/test_data/test_col_tao.npy", allow_pickle=True).item()
	struc_t           = np.load("Utils/test_data/test_struc_t.npy", allow_pickle=True)
	ts                = np.load("Utils/test_data/test_ts.npy", allow_pickle=True)
	taos              = np.load("Utils/test_data/test_taos.npy", allow_pickle=True)
	n_max             = np.load("Utils/test_data/test_n_max.npy", allow_pickle=True).item()
	n_min             = np.load("Utils/test_data/test_n_min.npy", allow_pickle=True).item()
	real_change       = np.load("Utils/test_data/test_change.npy", allow_pickle=True)
	real_time         = time.time()
	change = li.likelihoodloss(hic_dist_tao, row_tao, col_tao, struc_t, ts, taos, n_max, n_min)
	print("likelihoodloss", time.time() - real_time)
	assert(((real_change - change)<1e-9).all())

def test_likelihoodlossGPU():
	hic_dist_tao      = np.load("Utils/test_data/test_hic_dist_tao.npy", allow_pickle=True).item()
	row_tao           = np.load("Utils/test_data/test_row_tao.npy", allow_pickle=True).item()
	col_tao           = np.load("Utils/test_data/test_col_tao.npy", allow_pickle=True).item()
	struc_t           = cp.load("Utils/test_data/test_struc_t.npy", allow_pickle=True)
	ts                = cp.load("Utils/test_data/test_ts.npy", allow_pickle=True)
	taos              = cp.load("Utils/test_data/test_taos.npy", allow_pickle=True)
	n_max             = np.load("Utils/test_data/test_n_max.npy", allow_pickle=True).item()
	n_min             = np.load("Utils/test_data/test_n_min.npy", allow_pickle=True).item()
	real_change       = np.load("Utils/test_data/test_change.npy", allow_pickle=True)
	real_change       = cp.array(real_change)
	for i in hic_dist_tao.keys():
		hic_dist_tao[i] = cp.array(hic_dist_tao[i])
	#for i in row_tao.keys():
	#	row_tao[i] = cp.array(row_tao[i])
	#for i in col_tao.keys():
	#	col_tao[i] = cp.array(col_tao[i])
	real_time         = time.time()
	change = li.likelihoodlossGPU(hic_dist_tao, row_tao, col_tao, struc_t, ts, taos, n_max, n_min)
	print("likelihoodlossGPU", time.time() - real_time)
	assert(((real_change - change)<1e-9).all())

'''
def test_likelihoodlossGPUALT():
	hic_dist_tao      = np.load("Utils/test_data/test_hic_dist_tao.npy", allow_pickle=True).item()
	row_tao           = np.load("Utils/test_data/test_row_tao.npy", allow_pickle=True).item()
	col_tao           = np.load("Utils/test_data/test_col_tao.npy", allow_pickle=True).item()
	struc_t           = cp.load("Utils/test_data/test_struc_t.npy", allow_pickle=True)
	ts                = cp.load("Utils/test_data/test_ts.npy", allow_pickle=True)
	taos              = cp.load("Utils/test_data/test_taos.npy", allow_pickle=True)
	n_max             = np.load("Utils/test_data/test_n_max.npy", allow_pickle=True).item()
	n_min             = np.load("Utils/test_data/test_n_min.npy", allow_pickle=True).item()
	real_change       = np.load("Utils/test_data/test_change.npy", allow_pickle=True)
	real_change       = cp.array(real_change)
	for i in hic_dist_tao.keys():
		hic_dist_tao[i] = cp.array(hic_dist_tao[i])
	real_time         = time.time()
	change = li.likelihoodlossGPUALT(hic_dist_tao, row_tao, col_tao, struc_t, ts, taos, n_max, n_min)
	print("likelihoodlossGPUALT", time.time() - real_time)
	assert(((real_change - change)<1e-9).all())
'''
