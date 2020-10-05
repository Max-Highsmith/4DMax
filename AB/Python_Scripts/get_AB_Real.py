#This file contains code for extracting AB compartments from all time points in a structure
import time
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
import pdb
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import sys
sys.path.insert(0,"../")
from Utils import util as ut
import sys

hic_file = sys.argv[1]
out_file   = sys.argv[2]


start_time = time.time()

mat        = ut.loadConstraintAsMat(hic_file)
mat        = np.clip(mat, 0,30)
pear       = ma.corrcoef(ma.masked_invalid(mat))
pca        = PCA(n_components=1)
AB         = pca.fit_transform(pear)
AB_VEC     = np.squeeze(AB)
np.save(out_file, AB_VEC)
