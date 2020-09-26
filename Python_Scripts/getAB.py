#This file contains code for extracting AB compartments from all time points in a structure
import time
import numpy as np
import matplotlib.pyplot as plt
import pdb
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from Utils import util as ut
import sys

struc_file = sys.argv[1]
out_file   = sys.argv[2]


start_time = time.time()
struc      = np.load(struc_file)
AB_VEC     = np.zeros((struc.shape[0], struc.shape[1] ))

for i, ti in enumerate(range(0, struc.shape[0])):
	print("("+str(i)+"/"+str(struc.shape[0])+")"+":"+str(time.time() - start_time))
	struc_snap = struc[ti]
	contact    = ut.struc2contacts(struc_snap)
	pear       = np.corrcoef(np.log(contact))
	pca        = PCA(n_components=1)
	AB         = pca.fit_transform(pear)
	AB_VEC[i]  = np.squeeze(AB)

np.save(out_file, AB_VEC)
