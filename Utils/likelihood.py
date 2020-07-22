import Utils.util as ut
import time
import numpy as np

def getGradient(hic_dist, row, col, struc):
        start_time = time.time()
        wish_dist = ut.getWishDist(struc, row, col)
        n = hic_dist.shape[0]
        v = 0
        dl_ddk   = np.zeros(hic_dist.shape)
        ddk_dxyz = np.zeros((hic_dist.shape[0], 3))
        #print("time a", time.time()-start_time)
        start_time = time.time()

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


def getLikeChange(hic_dist_tao, row_tao, col_tao, struc_t, changea, changeb, t, struc_index, n_max, n_min):
        start = time.time()
        dl_ddk, ddk_dxyz = getGradient(hic_dist_tao[t],
                                        row_tao[t],
                                        col_tao[t],
                                        struc_t[struc_index])
        #print("getGradient:", time.time()-start)
        start = time.time()
        grada =  (ddk_dxyz.transpose()*dl_ddk).transpose()
        gradb = -(ddk_dxyz.transpose()*dl_ddk).transpose()
        changea = np.zeros(struc_t[struc_index].shape)
        changeb = np.zeros(struc_t[struc_index].shape)
        for i in range(0,3):
                changea[:,i] = np.bincount(row_tao[t],
                                weights=grada[:,i],
                                minlength=n_max-n_min+1)

                changeb[:,i] = np.bincount(col_tao[t],
                                weights=gradb[:,i],
                                minlength=n_max-n_min+1)

        #print("likeChange:", time.time()-start)
        return changea, changeb



def likelihoodloss(hic_dist_tao, row_tao, col_tao, struc_t, ts, taos, n_max, n_min):
        start = time.time()
        change  = np.zeros(struc_t.shape)
        changea = np.zeros(struc_t.shape)
        changeb = np.zeros(struc_t.shape)
        for t in ts:
                if float(t) in taos:
                        struc_index = np.where(ts==t)[0][0]
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
                        struc_index = np.where(ts==t)[0][0]
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
        print("likelihoodloss", time.time()-start)
        return -change

