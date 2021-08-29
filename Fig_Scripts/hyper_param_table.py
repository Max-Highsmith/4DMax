import glob
import pdb
import numpy as np
import matplotlib.pyplot as plt

etas = [1,1000,1000000]
lrs  = [0.1,0.001,0.0001,1e-05]
alphas = [0.6,0.8, 1.0]

table = []
for eta in etas:
    for lr in lrs:
        for alpha in alphas:

            loadstr = "".join(["Generated_Struc_Logs/",
                            "tuning_rep_1_eta_"+str(eta),
                            "_alpha_"+str(alpha),
                            "_lr_"+str(lr),
                            "_epoch_100_res_50000_step_21_chro_19.npy"])
            converged= len(glob.glob(loadstr)) == 1
            if converged:
                loadstr = sorted(glob.glob(loadstr))[0]
                x = np.load(loadstr,
                           allow_pickle=True)
                print(eta, lr, alpha)
                pcc_log = x.item()['pcc_log']
                last = pcc_log[-1]
                vals = np.stack(list(last.values()))[:,0]
                avg = np.max(vals)
                table.append([eta, lr, alpha, avg])
                print(avg)
            else:
                table.append([eta, lr, alpha, np.nan])
np.savetxt("hyper_param_results.csv", table,
        fmt='%i, %1.0e, %.1f, %1.4f', 
        delimiter=',', 
        header="eta,lr,alpha,avg_ pcc")
