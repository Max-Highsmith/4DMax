#This script will provide the HiC_Tool Tads for the orignal Contact maps
import pdb
import numpy as np
import sys
import matplotlib.pyplot as plt
sys.path.insert(0,"../")
from Utils import util as ut
TIME = 4

line=sys.argv[1]
day=sys.argv[2]
rep=sys.argv[3]
chro=sys.argv[4]
out_file=sys.argv[5]

#CONTACT_STRING = "../Real_Data/iPluripotent/day_D2_rep_1_chro_15"
CONTACT_STRING = "../Real_Data/"+str(line)+"/day_"+str(day)+"_rep_"+str(rep)+"_chro_"+str(chro)
mat            = ut.loadConstraintAsMat(CONTACT_STRING)
np.savetxt(out_file, mat, fmt='%0.2f', delimiter=' ')
