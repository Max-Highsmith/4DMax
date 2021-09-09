import torch
import numpy as np
from sklearn.decomposition import PCA
import numpy.ma as ma
import matplotlib.pyplot as plt
import pdb
import sys
sys.path.insert(0, "../")
from Utils import util as ut

chros         = [1,2,3,4,5,6,7,8,9,10,11,12,13,15,16,17,18,19]
missing_days  = [       2,   4,   6,   8]
days          = ['B','D2','D4','D6','D8','ES']
struc_times   = [  0,   4,   8,  12,  16,  20] 

struc_map     = {}
real_map      = {}
interp_map    = {}

real_o_e      = {}
struc_o_e     = {}
interp_o_e    = {}


real_pearson   = {}
struc_pearson  = {}
interp_pearson = {}

real_vec       = {}
struc_vec      = {}
interp_vec     = {}

for chro in chros:
    for day, missing_time, struc_time in zip(days[1:-1], missing_days, struc_times[1:-1]):
        print("interp", str(chro), str(missing_time), str(struc_time))
        interp_struc = np.load("".join([
                        "../Generated_Structures/",
                        "ipsc_missing_",
                        str(missing_time)+"_",
                        "rep_1",
                        "_eta_",
                        "1000",
                        "_alpha_",
                        "0.6",
                        "_lr_",
                        "0.0001",
                        "_epoch_",
                        "400",
                        "_res_",
                        "50000",
                        "_step_",
                        "21_chro_",
                        str(chro),
                        ".npy"]))
        interp_map[struc_time] = ut.struc2contacts(interp_struc[struc_time])
        interp_map_torch = torch.from_numpy(interp_map[struc_time])
        interp_map_torch = interp_map_torch.unsqueeze(0).unsqueeze(0)
        resized_interp_map = torch.nn.functional.avg_pool2d(interp_map_torch,  kernel_size=2)
        resized_interp_map = resized_interp_map.squeeze()
        interp_map[struc_time] = resized_interp_map.numpy()

    for day in days:
        print(str(chro),str(day))
        real_map[day]    = ut.loadConstraintAsMat("../Real_Data/iPluripotent/day_"+str(day)+"_rep_1_chro_"+str(chro))
        real_map_torch   = torch.from_numpy(real_map[day])
        real_map_torch   = real_map_torch.unsqueeze(0).unsqueeze(0)
        resized_real_map = torch.nn.functional.avg_pool2d(real_map_torch, kernel_size=2)
        resized_real_map = resized_real_map.squeeze()
        real_map[day]    = resized_real_map.numpy()

    struc = np.load("../Generated_Structures/ipsc_full_rep_1_eta_1000_alpha_0.6_lr_0.0001_epoch_400_res_50000_step_21_chro_"+str(chro)+".npy")
    for struc_time in struc_times:
        print(str(chro), str(struc_time))
        struc_map[struc_time] = ut.struc2contacts(struc[struc_time])
        struc_map_torch        = torch.from_numpy(struc_map[struc_time])
        struc_map_torch        = struc_map_torch.unsqueeze(0).unsqueeze(0)
        resized_struc_map      = torch.nn.functional.avg_pool2d(struc_map_torch, kernel_size=2)
        resized_struc_map      = resized_struc_map.squeeze()
        struc_map[struc_time]  = resized_struc_map.numpy()
    
    not_valid = []
    for day in days:
        not_valid.extend(np.where(np.diagonal(real_map[day])==0)[0])
    for day in days:
        real_map[day]  = np.delete(np.delete(real_map[day], not_valid, axis=0), not_valid, axis=1)
    for struc_time in struc_times:
        struc_map[struc_time] = np.delete(np.delete(struc_map[struc_time], not_valid, axis=0), not_valid, axis=1)
    for interp_time in struc_times[1:-1]:
        interp_map[interp_time] = np.delete(np.delete(interp_map[interp_time], not_valid, axis=0), not_valid, axis=1)

    for day in days:
        expected  = np.zeros(real_map[day].shape)
        I_S_val   = np.zeros(real_map[day].shape[0])
        I_S_count = np.zeros(real_map[day].shape[0])
        for i in range(0, real_map[day].shape[0]):
            for j in range(0, real_map[day].shape[0]):
                indx = np.abs(i-j)
                I_S_val[indx]   += real_map[day][i,j]
                I_S_count[indx] += 1

        I_func       = I_S_val       / I_S_count
        for i in range(0, real_map[day].shape[0]):
            for j in range(0, real_map[day].shape[0]):
                indx = np.abs(i-j)
                expected[i,j] = I_func[indx]

        real_o_e[day]      = ma.masked_invalid(real_map[day]/expected)
        real_pearson[day]  = ma.cov(np.clip(real_o_e[day],0,2))
        pca                = PCA(n_components=1)
        ab                 = pca.fit_transform(real_pearson[day])
        real_vec[day]      = np.squeeze(ab)
        np.save("Full_AB_Vecs/real_vec_day_"+str(day)+"_chro_"+str(chro)+".npy", real_vec[day])

    for time in struc_times:
        expected  = np.zeros(struc_map[time].shape)
        I_S_val   = np.zeros(struc_map[time].shape[0])
        I_S_count = np.zeros(struc_map[time].shape[0])
        for i in range(0, struc_map[time].shape[0]):
            for j in range(0, struc_map[time].shape[0]):
                indx = np.abs(i-j)
                I_S_val[indx]   += struc_map[time][i,j]
                I_S_count[indx] += 1

        I_func       = I_S_val       / I_S_count
        for i in range(0, struc_map[time].shape[0]):
            for j in range(0, struc_map[time].shape[0]):
                indx = np.abs(i-j)
                expected[i,j] = I_func[indx]

        struc_o_e[time]     = ma.masked_invalid(struc_map[time]/expected)
        struc_pearson[time] = ma.cov(np.clip(struc_o_e[time],0,2))
        pca                 = PCA(n_components=1)
        ab                  = pca.fit_transform(struc_pearson[time])
        struc_vec[time]     = np.squeeze(ab)
        np.save("Full_AB_Vecs/struc_vec_time_"+str(time)+"_chro_"+str(chro)+".npy", struc_vec[time])
                
    for time in struc_times[1:-1]:
        print("building interp time"+str(time))
        expected  = np.zeros(interp_map[time].shape)
        I_S_val   = np.zeros(interp_map[time].shape[0])
        I_S_count = np.zeros(interp_map[time].shape[0])
        for i in range(0, interp_map[time].shape[0]):
            for j in range(0, interp_map[time].shape[0]):
                indx = np.abs(i-j)
                I_S_val[indx]   += interp_map[time][i,j]
                I_S_count[indx] += 1

        I_func       = I_S_val       / I_S_count
        for i in range(0, interp_map[time].shape[0]):
            for j in range(0, interp_map[time].shape[0]):
                indx = np.abs(i-j)
                expected[i,j] = I_func[indx]

        interp_o_e[time]     = ma.masked_invalid(interp_map[time]/expected)
        interp_pearson[time] = ma.cov(np.clip(interp_o_e[time],0,2))
        pca                 = PCA(n_components=1)
        ab                  = pca.fit_transform(interp_pearson[time])
        interp_vec[time]     = np.squeeze(ab)
        np.save("Full_AB_Vecs/interp_vec_time_"+str(time)+"_chro_"+str(chro)+".npy", interp_vec[time])


'''
			np.save("AB_Vecs/real_day_"+str(day)+ "_missing_"+str(missing)+"_time_"+str(missing_time)+"_chro_"+str(chro), vec)
			np.save("AB_Vecs/struc_day_"+str(day)+"_missing_"+str(missing)+"_time_"+str(missing_time)+"_chro_"+str(chro), vec_struc)
			fig, ax = plt.subplots(3,2)
			ax[0,0].imshow(np.clip(o_e,0,2), cmap="RdBu")
			ax[1,0].imshow(np.clip(pearson,-.1,.1), cmap="RdBu")
			ax[2,0].bar(list(range(0,vec.shape[0])), vec)
			ax[0,1].imshow(np.clip(o_e_struc,0,2), cmap="RdBu")
			ax[1,1].imshow(np.clip(pearson_struc,-.1,.1), cmap="RdBu")
			ax[2,1].bar(list(range(0,vec_struc.shape[0])), vec_struc)
			plt.savefig("Pearson/fig_chro_"+str(chro)+"_day_"+str(day)+"_missing_"+str(missing)+"_time_"+str(missing_time)+".png")
			np.save("Pearson/real_chro_"+str(chro)+"_day_"+str(day)+"_missing_"+str(missing)+"_time_"+str(missing_time), pearson.data)
			np.save("Pearson/struc_chro_"+str(chro)+"_day_"+str(day)+"_missing_"+str(missing)+"_time_"+str(missing_time), pearson_struc.data)
			plt.close()
			plt.clf()
			plt.cla()
'''
