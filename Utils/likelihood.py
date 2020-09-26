import pdb
import Utils.util as ut
#import util as ut
import time
import numpy as np
import cupy as cp


def getGradientGPU(hic_dist, row, col, struc):
        start_time = time.time()
        wish_dist = ut.getWishDist(struc, row, col)
        n = hic_dist.shape[0]
        v = 0
        dl_ddk   = cp.zeros(hic_dist.shape)
        ddk_dxyz = cp.zeros((hic_dist.shape[0], 3))
        #print("time a", time.time()-start_time)
        start_time = time.time()

        diff = cp.abs(wish_dist-hic_dist)
        v    = cp.sum(diff)
        #print("time b",time.time()-start_time)
        start_time = time.time()

        dl_ddk = (n*(hic_dist-wish_dist))/v
        denoms = cp.linalg.norm(struc[row]-struc[col], axis=1)
        ddk_dxyz = ((struc[row]-struc[col]).transpose()/denoms).transpose()
        ddk_dxyz[cp.abs(denoms)<.001] = cp.zeros(3)
        #print("alt c",time.time()-start_time)
        start_time = time.time()
        return dl_ddk, ddk_dxyz

def getGradient(hic_dist, row, col, struc):
        start_time = time.time()
        wish_dist = ut.getWishDist(struc, row, col)
        n = hic_dist.shape[0]
        v = 0
        dl_ddk   = np.zeros(hic_dist.shape)
        ddk_dxyz = np.zeros((hic_dist.shape[0], 3))
        #print("time a", time.time()-start_time)
        #start_time = time.time()

        diff = np.abs(wish_dist-hic_dist)
        v    = np.sum(diff)
        #print("time b",time.time()-start_time)
        start_time = time.time()

        dl_ddk = (n*(hic_dist-wish_dist))/v
        denoms = np.linalg.norm(struc[row]-struc[col], axis=1)
        ddk_dxyz = ((struc[row]-struc[col]).transpose()/denoms).transpose()
        ddk_dxyz[np.abs(denoms)<.001] = np.zeros(3)
        #print("alt c",time.time()-start_time)
        start_time = time.time()
        return dl_ddk, ddk_dxyz


#TODO TODO TODO GPU
def getLikeChangeGPU(hic_dist_tao, row_tao, col_tao, struc_t, changea, changeb, t, struc_index, n_max, n_min):
        start = time.time()
        #print("THESE VALS", str(type(hic_dist_tao[0])), str(type(row_tao[0])), str(type(col_tao[0])), str(type(struc_t[0])))
        dl_ddk, ddk_dxyz = getGradientGPU(hic_dist_tao[t],
                                        row_tao[t],
                                        col_tao[t],
                                        struc_t[struc_index])
        start = time.time()
        grada =  (ddk_dxyz.transpose()*dl_ddk).transpose()
        gradb = -(ddk_dxyz.transpose()*dl_ddk).transpose()
        start = time.time()
        changea = np.zeros(struc_t[struc_index].shape)
        changeb = np.zeros(struc_t[struc_index].shape)
        for i in range(0,3):
                start = time.time()
                changea[:,i] = np.bincount(row_tao[t],
                                weights=cp.asnumpy(grada[:,i]),
                                minlength=n_max-n_min+1)

                changeb[:,i] = np.bincount(col_tao[t],
                                weights=cp.asnumpy(gradb[:,i]),
                                minlength=n_max-n_min+1)

        return cp.array(changea), cp.array(changeb)



def getLikeChange(hic_dist_tao, row_tao, col_tao, struc_t, changea, changeb, t, struc_index, n_max, n_min):
        start = time.time()
        dl_ddk, ddk_dxyz = getGradient(hic_dist_tao[t],
                                        row_tao[t],
                                        col_tao[t],
                                        struc_t[struc_index])
        start = time.time()
        grada =  (ddk_dxyz.transpose()*dl_ddk).transpose()
        gradb = -(ddk_dxyz.transpose()*dl_ddk).transpose()
        start = time.time()
        changea = np.zeros(struc_t[struc_index].shape)
        changeb = np.zeros(struc_t[struc_index].shape)
        for i in range(0,3):
                start = time.time()
                changea[:,i] = np.bincount(row_tao[t],
                                weights=grada[:,i],
                                minlength=n_max-n_min+1)

                changeb[:,i] = np.bincount(col_tao[t],
                                weights=gradb[:,i],
                                minlength=n_max-n_min+1)
        return changea, changeb


#TODO
def likelihoodlossGPU(hic_dist_tao, row_tao, col_tao, struc_t, ts, taos, n_max, n_min):	
        start = time.time()
        change  = cp.zeros(struc_t.shape)
        changea = cp.zeros(struc_t.shape)
        changeb = cp.zeros(struc_t.shape)
        print("timea:",time.time()-start) 
        for t in ts:
                start = time.time()
                tt = t.item()
                struc_index = cp.where(ts==t)[0][0].item()
                if float(t) in taos:
                        changea[struc_index], changeb[struc_index] = getLikeChangeGPU(hic_dist_tao,
                                                row_tao,
                                                col_tao,
                                                struc_t,
                                                changea,
                                                changeb,
                                                tt,
                                                struc_index,
						n_max, 
						n_min)
                else:
                        lower = taos[taos -tt<0]
                        upper = taos[taos -tt>0]
                        a1    = lower[cp.argmin(cp.abs(lower-tt))]
                        a2    = upper[cp.argmin(cp.abs(upper-tt))]
                        w2    = (tt-a1)/cp.abs(a1-a2)
                        w1    = (a2-tt)/cp.abs(a1-a2)
                        #print(a1,a2,w1,w2)
                        changea1, changeb1 = getLikeChangeGPU(hic_dist_tao,
                                                        row_tao,
                                                        col_tao,
                                                        struc_t,
                                                        changea,
                                                        changeb,
                                                        a1.item(),
                                                        struc_index,
							n_max,
							n_min)

                        changea2, changeb2 = getLikeChangeGPU(hic_dist_tao,
                                                        row_tao,
                                                        col_tao,
                                                        struc_t,
                                                        changea,
                                                        changeb,
                                                        a2.item(),
                                                        struc_index,
							n_max,
							n_min)
                        changea[struc_index] += w1*changea1+w2*changea2
                        changeb[struc_index] += w1*changeb1+w2*changeb2
                #print("timeb", str(time.time()-start))
        change = changea+changeb
        return -change



def likelihoodloss(hic_dist_tao, row_tao, col_tao, struc_t, ts, taos, n_max, n_min):
        start = time.time()
        change  = np.zeros(struc_t.shape)
        changea = np.zeros(struc_t.shape)
        changeb = np.zeros(struc_t.shape)
        for t in ts:	
                struc_index = np.where(ts==t)[0][0]
                if float(t) in taos:
                        changea[struc_index], changeb[struc_index] = getLikeChange(hic_dist_tao,
                                                row_tao,
                                                col_tao,
                                                struc_t,
                                                changea,
                                                changeb,
                                                t,
                                                struc_index,
						n_max, 
						n_min)
                else:
                        lower = taos[taos -t<0]
                        upper = taos[taos -t>0]
                        a1    = lower[np.argmin(np.abs(lower-t))]
                        a2    = upper[np.argmin(np.abs(upper-t))]
                        w2    = (t-a1)/np.abs(a1-a2)
                        w1    = (a2-t)/np.abs(a1-a2)
                        #print(a1,a2,w1,w2)
                        changea1, changeb1 = getLikeChange(hic_dist_tao,
                                                        row_tao,
                                                        col_tao,
                                                        struc_t,
                                                        changea,
                                                        changeb,
                                                        a1,
                                                        struc_index,
							n_max,
							n_min)

                        changea2, changeb2 = getLikeChange(hic_dist_tao,
                                                        row_tao,
                                                        col_tao,
                                                        struc_t,
                                                        changea,
                                                        changeb,
                                                        a2,
                                                        struc_index,
							n_max,
							n_min)
                        changea[struc_index] += w1*changea1+w2*changea2
                        changeb[struc_index] += w1*changeb1+w2*changeb2
        change = changea+changeb
        #print("likelihoodloss", time.time()-start)
        return -change


#TODO
def likelihoodlossGPUALT(hic_dist_tao, row_tao, col_tao, struc_t, ts, taos, n_max, n_min):
        start = time.time()
        change  = cp.zeros(struc_t.shape)
        changea = cp.zeros(struc_t.shape)
        changeb = cp.zeros(struc_t.shape)
        print("timea:",time.time()-start)
        #for t in ts:
        def helperGetLikeChangeGPU(t):
                t = cp.array(t)
                start = time.time()
                tt = t.item()
                struc_index = cp.where(ts==t)[0][0].item()
                if float(t) in taos:
                        change_a_t, change_b_t = getLikeChangeGPU(hic_dist_tao,
                                                row_tao,
                                                col_tao,
                                                struc_t,
                                                changea,
                                                changeb,
                                                tt,
                                                struc_index,
						n_max, 
						n_min)
                else:
                        lower = taos[taos -tt<0]
                        upper = taos[taos -tt>0]
                        a1    = lower[cp.argmin(cp.abs(lower-tt))]
                        a2    = upper[cp.argmin(cp.abs(upper-tt))]
                        w2    = (tt-a1)/cp.abs(a1-a2)
                        w1    = (a2-tt)/cp.abs(a1-a2)
                        changea1, changeb1 = getLikeChangeGPU(hic_dist_tao,
                                                        row_tao,
                                                        col_tao,
                                                        struc_t,
                                                        changea,
                                                        changeb,
                                                        a1.item(),
                                                        struc_index,
							n_max,
							n_min)

                        changea2, changeb2 = getLikeChangeGPU(hic_dist_tao,
                                                        row_tao,
                                                        col_tao,
                                                        struc_t,
                                                        changea,
                                                        changeb,
                                                        a2.item(),
                                                        struc_index,
							n_max,
							n_min)
                        change_a_t   = w1*changea1+w2*changea2
                        change_b_t   = w1*changeb1+w2*changeb2	
                change_t = change_a_t + change_b_t
                print("indiv", str(start - time.time()))
                return cp.asnumpy(change_t)
        altt   = np.frompyfunc(helperGetLikeChangeGPU,1,1)
        change = altt(cp.asnumpy(ts)) 
        change  = cp.array(change)
        #change = cp.array(list(map(helperGetLikeChangeGPU, ts)))
        #change = cp.array([helperGerLikeChangeGPU for t in ts])
        #change = changea+changeb
        return -change


