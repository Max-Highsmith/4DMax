import matplotlib.pyplot as plt
import numpy as np
import pdb
import sys
from Utils import util as ut

struc_name = sys.argv[1]
time       = int(sys.argv[2])
ref_map    = sys.argv[3]
res        = int(sys.argv[4])

struc      = np.load(struc_name)
mat        = ut.struc2contacts(struc[time])

x          = np.loadtxt(ref_map)
row        = x[:,0].astype(int)
col        = x[:,1].astype(int)
ifs        = x[:,2].astype(float)
row = (row/res).astype(int)
col = (col/res).astype(int)
real_mat = ut.constraints2mats(row, col, ifs)

pdb.set_trace()
plt.imshow(np.log(real_mat), cmap="Reds")
plt.show()
