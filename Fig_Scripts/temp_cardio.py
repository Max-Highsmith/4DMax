import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from Utils import util as ut

x = np.load("Generated_Structures/cardio_full_rep_1_eta_1000_alpha_0.6_lr_1e-05_epoch_1000_res_1_step_15_chro_15.npy")
for i in range(0,14):
	ut.show_struc_indiv(x[i])

