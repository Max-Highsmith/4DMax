import torch
import numpy as np
from sklearn.decomposition import PCA
import numpy.ma as ma
import matplotlib.pyplot as plt
import pdb
import sys
sys.path.insert(0, "../")
from Utils import util as ut

chros         = [11,12,13,14,15,16,17,18]#19, 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
days          = ['B','D2','D4','D6','D8','ES']
missings = [2,4,6,8]
missing_times = [4,8,12,16] 
for chro in chros:
	for missing, missing_time in zip(missings, missing_times):
		for day in days:
			print(str(chro), str(day), str(missing))
			#chro         = 3
			#day          = 'D2'
			#missing      = 2
			#missing_time = 4
			real_map   = ut.loadConstraintAsMat("../Real_Data/iPluripotent/day_"+str(day)+"_rep_1_chro_"+str(chro))
			struc      = np.load("../Generated_Structures/ipsc_missing_"+str(missing)+"_rep_1_eta_1000_alpha_0.6_lr_0.0001_epoch_400_res_50000_step_21_chro_"+str(chro)+".npy")
			struc_map  = ut.struc2contacts(struc[missing_time])


			#shrink to 100kb
			real_map_torch   = torch.from_numpy(real_map)
			real_map_torch   = real_map_torch.unsqueeze(0).unsqueeze(0)
			resized_real_map = torch.nn.functional.avg_pool2d(real_map_torch, kernel_size=2)
			resized_real_map = resized_real_map.squeeze()
			real_map = resized_real_map.numpy()

			struc_map_torch   = torch.from_numpy(struc_map)
			struc_map_torch   = struc_map_torch.unsqueeze(0).unsqueeze(0)
			resized_struc_map = torch.nn.functional.avg_pool2d(struc_map_torch, kernel_size=2)
			resized_struc_map = resized_struc_map.squeeze()
			struc_map         = resized_struc_map.numpy()


			#impute
			end_valid = np.where(np.diagonal(real_map)==0)[0]
			real_map  = np.delete(np.delete(real_map,  end_valid, axis=0), end_valid, axis=1)
			struc_map = np.delete(np.delete(struc_map, end_valid, axis=0), end_valid, axis=1)


			expected   = np.zeros(real_map.shape)
			I_S_val    = np.zeros(real_map.shape[0])
			I_S_count  = np.zeros(real_map.shape[0])
			for i in range(0, real_map.shape[0]):
				#print(i)
				for j in range(0, real_map.shape[0]):
					indx = np.abs(i-j)
					I_S_val[indx]   += real_map[i,j]
					I_S_count[indx] += 1



			expected_struc   = np.zeros(struc_map.shape)
			I_S_val_struc    = np.zeros(struc_map.shape[0])
			I_S_count_struc  = np.zeros(struc_map.shape[0])
			for i in range(0, struc_map.shape[0]):
				#print(i)
				for j in range(0, struc_map.shape[0]):
					indx = np.abs(i-j)
					I_S_val_struc [indx]   += struc_map[i,j]
					I_S_count_struc[indx]  += 1

			I_func_struc = I_S_val_struc / I_S_count_struc
			I_func       = I_S_val       / I_S_count

			for i in range(0, real_map.shape[0]):
				#print(i)
				for j in range(0, real_map.shape[0]):
					indx = np.abs(i-j)
					expected[i,j] = I_func[indx]

			for i in range(0, struc_map.shape[0]):
				#print(i)
				for j in range(0, struc_map.shape[0]):
					indx = np.abs(i-j)
					expected_struc[i,j] = I_func_struc[indx]


			o_e     = ma.masked_invalid(real_map/expected)
			pearson = ma.cov(np.clip(o_e,0,2))

			o_e_struc     = ma.masked_invalid(struc_map/expected_struc)
			pearson_struc = ma.cov(np.clip(o_e_struc,0,2))




			#PCA
			pca = PCA(n_components=1)
			ab  = pca.fit_transform(pearson)
			vec = np.squeeze(ab)

			pca_struc = PCA(n_components=1)
			ab_struc  = pca.fit_transform(pearson_struc)
			vec_struc = np.squeeze(ab_struc)

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
