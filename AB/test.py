from sklearn.decomposition import PCA
import sys
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
import pdb
sys.path.insert(0, "../")
from Utils import util as ut

chro = "13"

struc     = np.load("../Generated_Structures/ipsc_missing_2_rep_1_eta_1000_alpha_0.6_lr_0.0001_epoch_400_res_50000_step_21_chro_"+str(chro)+".npy")
real_map  = ut.loadConstraintAsMat("../Real_Data/iPluripotent/day_D2_rep_1_chro_"+str(chro))
struc_map = ut.struc2contacts(struc[4])
struc_map = np.clip(struc_map, 0, 10)
real_map  = np.clip(real_map, 0, 30)
real_pear = ma.corrcoef(ma.masked_invalid(real_map))
struc_pear= ma.corrcoef(ma.masked_invalid(struc_map))

pca_real   = PCA(n_components=1)
pca_struc  = PCA(n_components=1)
ab_real    = pca_real.fit_transform(real_pear)
ab_struc   = pca_struc.fit_transform(struc_pear)
real_vec   = np.squeeze(ab_real)
struc_vec  = np.squeeze(ab_struc)

fig, ax = plt.subplots(3,2)
ax[0,0].imshow(np.clip(struc_map,0,10), cmap="Reds")
ax[0,1].imshow(np.clip(real_map,0,30), cmap="Reds")
ax[1,0].imshow(np.clip(struc_pear,0,10), cmap="Blues")
ax[1,1].imshow(np.clip(real_pear,0,30), cmap="Blues")
ax[2,0].bar(list(range(0, struc_vec.shape[0])),struc_vec)
ax[2,1].bar(list(range(0, struc_vec.shape[0])),real_vec)
plt.show()



pdb.set_trace()
