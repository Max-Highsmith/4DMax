#this script is to address a reviewer request for simple interpolation of contact maps without using 4dmax
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
import numpy as np
import pdb
import sys
sys.path.append(".")
import Utils.util as ut


days     = ['Ba','D2','D4','D6','D8']
gran_pos = [0,4,8,12,16,20]
results  = []
for chro in list(range(1,20)):#14
    print("chro", str(chro))
    real_days   = []
    real_days_2 = []
    recon_days  = []
    simple_days = {}
    interp_days = {}
    for d, day in enumerate(days):
        print(d)
        real_days.append(ut.loadConstraintAsMat("Real_Data/iPluripotent/day_"+str(day)+"_rep_1_chro_"+str(chro)))
        print("load real")
        real_days_2.append(ut.loadConstraintAsMat("Real_Data/iPluripotent/day_"+str(day)+"_rep_2_chro_"+str(chro)))
        print("load other real")
        recon_str = "".join(["Generated_Structures",
            "/ipsc_full_rep_1_eta_1000_alpha_0.6_lr_0.0001_epoch_400_res_50000_step_21_chro_",
            str(chro),
            ".npy"])
        recon_days.append(ut.loadStrucAtTimeAsMat(recon_str, gran_pos[d]))
        print("load recon")
    simple_days = {}

    for d, day in enumerate([2,4,6]):
        #interp_str = "".join(["Generated_Structures",
        #    "/ipsc_full_rep_1_eta_1000_alpha_0.6_lr_0.0001_epoch_400_res_50000_step_21_chro_",
        #    str(chro),
        #    ".npy"])

        interp_str = "".join(["Generated_Structures",
            "/ipsc_missing_"+str(day)+"_rep_1_eta_1000_alpha_0.6_lr_0.0001_epoch_400_res_50000_step_21_chro_",
            str(chro),
            ".npy"])
        interp_days[d+1] = ut.loadStrucAtTimeAsMat(interp_str, d)
        print("load interp")

        buff = recon_days[d+1].shape[0]-real_days[d+1].shape[0]
        if buff>0:
            interp_days[d+1]=interp_days[d+1][:-buff, :-buff]
            recon_days[d+1]=recon_days[d+1][:-buff, :-buff]

    simple_days[1] = (real_days[0]+real_days[2])/2
    simple_days[2] = (real_days[1]+real_days[3])/2
    simple_days[3] = (real_days[2]+real_days[4])/2

    cur_results = np.zeros((4,3))
    for t, time in enumerate([1,2,3]):
        ignore_these = np.diag(real_days[time])==0
        temp_real   = np.delete(np.delete(real_days[time], ignore_these, axis=0), 
                ignore_these, axis=1)
        temp_real_2 = np.delete(np.delete(real_days_2[time], ignore_these, axis=0),
                ignore_these, axis=1)
        temp_simple = np.delete(np.delete(simple_days[time], ignore_these, axis=0),
                ignore_these, axis=1)
        temp_recon = np.delete(np.delete(recon_days[time], ignore_these, axis=0),
                ignore_these, axis=1)
        temp_interp = np.delete(np.delete(interp_days[time], ignore_these, axis=0),
                ignore_these, axis=1)
        cur_results[0,t] = spearmanr(temp_real, temp_real_2, axis=None)[0]
        cur_results[1,t] = spearmanr(temp_real, temp_simple, axis=None)[0]
        cur_results[2,t] = spearmanr(temp_real, temp_recon, axis=None)[0]
        cur_results[3,t] = spearmanr(temp_real, temp_interp, axis=None)[0]
    results.append(cur_results)
    np.save("_fresh_simple_interp_results.txt", results)
    
    
results = np.stack(results)
np.save("_fresh_simple_interp_results.txt", results)
pdb.set_erace()
