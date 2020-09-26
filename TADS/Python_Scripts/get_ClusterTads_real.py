import numpy as np
import pdb
import glob
import sys

in_dir    = sys.argv[1]
out_file  = sys.argv[2]

bestCluster = glob.glob(in_dir+"/TADs/Be*")
tads        = np.loadtxt(bestCluster[0],str, skiprows=1)
tad_vals = tads[:,(1,3)].astype(int)
np.save(out_file, tad_vals)
