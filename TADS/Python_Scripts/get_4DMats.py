import os
import matplotlib.pyplot as plt
import sys
sys.path.insert(0,"../")
from Utils import util as ut
import time
import numpy as np
import pdb
import sys

struc_file = sys.argv[1]
out_dir   = sys.argv[2]

if not os.path.exists(out_dir):
	os.mkdir(out_dir)
start_time = time.time()
struc      = np.load(struc_file)
for i, ti in enumerate(range(0, struc.shape[0])):
	print("("+str(i)+"/"+str(struc.shape[0])+")"+":"+str(time.time() - start_time))
	struc_snap = struc[ti]
	contact    = ut.struc2contacts(struc_snap)
	np.savetxt(out_dir+"/mat_time_"+str(i), contact, fmt='%0.2f', delimiter=' ')

