from sklearn.decomposition import PCA
from Utils import util as ut
import numpy as np
import matplotlib.pyplot as plt
import pdb
x = np.loadtxt("Real_Data/iPluripotent/day_D4_rep_1_chro_15")
res  = 50000
rows = x[:,0].astype(int)
cols = x[:,1].astype(int)
vals = x[:,2].astype(float)
rows = rows/res
cols = cols/res
rows = rows.astype(int)
cols = cols.astype(int)
mat  = ut.constraints2mats(rows, cols, vals)
epsilon = 1
pdb.set_trace()
pear = np.corrcoef(mat+epsilon)
pca  = PCA(n_components=1)
AB   = pca.fit_transform(pear)
plt.bar(list(range(0, AB.shape[0])), np.squeeze(AB), color="deeppink")
pdb.set_trace()
