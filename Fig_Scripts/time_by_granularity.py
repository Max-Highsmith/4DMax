import pdb
import numpy as np
import matplotlib.pyplot as plt


#cardio
steps    = np.array([15,29,43,57,71])
times    = np.zeros(steps.shape[0])
num_bins = np.zeros(steps.shape[0])
for s, step in enumerate(steps):
	item        = np.load("Generated_Struc_Logs/cardio_full_rep_1_eta_1000_alpha_0.6_lr_0.0001_epoch_400_res_1_step_"+str(step)+"_chro_10.npy", allow_pickle=True).item()
	times[s]    = np.sum(item['time'])
	steps[s]    = step

fig, ax = plt.subplots(1)
ax.set_xlabel("Granularity")
ax.set_ylabel("Time to 4D Model Generation (seconds)")
ax.set_title("Cardio Time (400 epochs chro 10)")
ax.scatter(steps, times, color='darkviolet')

plt.savefig("Figures/Timing/timing_cardio_by_step.png")

plt.cla()
plt.clf()
plt.close()

#cardio
steps    = np.array([11,21,31,41,51])
times    = np.zeros(steps.shape[0])
num_bins = np.zeros(steps.shape[0])
for s, step in enumerate(steps):
	item        = np.load("Generated_Struc_Logs/ipsc_full_rep_1_eta_1000_alpha_0.6_lr_0.0001_epoch_400_res_50000_step_"+str(step)+"_chro_10.npy", allow_pickle=True).item()
	times[s]    = np.sum(item['time'])
	steps[s]    = step

fig, ax = plt.subplots(1)
ax.set_xlabel("Granularity")
ax.set_ylabel("Time to 4D Model Generation (seconds)")
ax.set_title("iPSC Time (400 epochs chro 10)")
ax.scatter(steps, times, color='turquoise')
plt.savefig("Figures/Timing/timing_ipsc_by_step.png")

