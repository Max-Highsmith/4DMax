import shutil
import subprocess
import natsort
import glob
import time
import numpy as np
import sys
import os
import pdb

in_file     = sys.argv[1]
chro       = sys.argv[2]
res        = sys.argv[3]
out_file   = sys.argv[4]

tad_vals   = {}

command = "python2.7 Other_Tools/HiCtool_TAD_analysis.py --res="+str(res)+" --action=\"full_tad_analysis\""+" -i "+str(in_file)+" -c \"Other_Tools/chromSizes/\""+" -s \"hg38\" --isGlobal=\"0\" --tab_sep=1 --chr="+str(chro)+" --data_type=normaized"
subprocess.call(command, shell=True)
tad_file      = "HiCtool_chr"+str(chro)+"_topological_domains.txt"
tad_vals_snap = np.loadtxt(tad_file, int)
tad_vals   = tad_vals_snap
	#subprocess.call("mv HiCtool_chr"+str(chro)+"*_topological_domains.txt"+str(out_dir)+"/chro_"+str(chro)+str(, shell=True)
np.save(out_file, tad_vals)

DI_file = "HiCtool_chr"+str(chro)+"_DI.txt"
hmm_file = "HiCtool_chr"+str(chro)+"_hmm_states.txt"

shutil.copy(DI_file, out_file.split(".")[0]+"_DI.txt")
shutil.copy(hmm_file, out_file.split(".")[0]+"_hmm.txt")

