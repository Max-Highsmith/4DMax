import pdb
import numpy as np
import matplotlib.pyplot as plt


#cardio
chros    = np.array(range(1,22))
times    = np.zeros(chros.shape[0])
num_bins = np.zeros(chros.shape[0])
for c, chro in enumerate(chros):
	item        = np.load("Generated_Struc_Logs/cardio_full_rep_1_eta_1000_alpha_0.6_lr_0.0001_epoch_400_res_1_step_15_chro_"+str(chro)+".npy", allow_pickle=True).item()
	binsize     = np.load("Generated_Structures/cardio_full_rep_1_eta_1000_alpha_0.6_lr_0.0001_epoch_400_res_1_step_15_chro_"+str(chro)+".npy").shape[1]
	times[c]    = np.sum(item['time'])
	num_bins[c] = binsize

fig, ax = plt.subplots(1)
ax.set_xlabel("Bin Length")
ax.set_ylabel("Time to 4D Model Generation (seconds)")
ax.set_title("Cardio Time (400 epochs 15 steps)")
ax.scatter(num_bins, times, color='darkviolet')

plt.savefig("Figures/Timing/timing_cardio_by_bin.png")

plt.cla()
plt.clf()
plt.close()


chros    = np.array(range(1,19))
times    = np.zeros(chros.shape[0])
num_bins = np.zeros(chros.shape[0])
for c, chro in enumerate(chros):
	item        = np.load("Generated_Struc_Logs/ipsc_full_rep_1_eta_1000_alpha_0.6_lr_0.0001_epoch_400_res_50000_step_21_chro_"+str(chro)+".npy", allow_pickle=True).item()
	binsize     = np.load("Generated_Structures/ipsc_full_rep_1_eta_1000_alpha_0.6_lr_0.0001_epoch_400_res_50000_step_21_chro_"+str(chro)+".npy").shape[1]
	times[c]    = np.sum(item['time'])
	num_bins[c] = binsize

fig, ax = plt.subplots(1)
ax.set_xlabel("Bin Length")
ax.set_ylabel("Time to 4D Model Generation (seconds)")
ax.set_title("iPSC Time (400 epochs 21 steps)")
ax.scatter(num_bins, times, color='aqua')
plt.savefig("Figures/Timing/timing_ipsc_by_bin.png")


#combined
chros    = np.array(range(1,22))
times    = np.zeros(chros.shape[0])
num_bins = np.zeros(chros.shape[0])
for c, chro in enumerate(chros):
	item        = np.load("Generated_Struc_Logs/cardio_full_rep_1_eta_1000_alpha_0.6_lr_0.0001_epoch_400_res_1_step_15_chro_"+str(chro)+".npy", allow_pickle=True).item()
	binsize     = np.load("Generated_Structures/cardio_full_rep_1_eta_1000_alpha_0.6_lr_0.0001_epoch_400_res_1_step_15_chro_"+str(chro)+".npy").shape[1]
	times[c]    = np.sum(item['time'])
	num_bins[c] = binsize

fig, ax = plt.subplots(1)
ax.set_title("Time (400 epochs)")
ax.scatter(num_bins, times, color='darkviolet')

chros    = np.array(range(1,19))
times    = np.zeros(chros.shape[0])
num_bins = np.zeros(chros.shape[0])
for c, chro in enumerate(chros):
	item        = np.load("Generated_Struc_Logs/ipsc_full_rep_1_eta_1000_alpha_0.6_lr_0.0001_epoch_400_res_50000_step_21_chro_"+str(chro)+".npy", allow_pickle=True).item()
	binsize     = np.load("Generated_Structures/ipsc_full_rep_1_eta_1000_alpha_0.6_lr_0.0001_epoch_400_res_50000_step_21_chro_"+str(chro)+".npy").shape[1]
	times[c]    = np.sum(item['time'])
	num_bins[c] = binsize

ax.set_xlabel("Bin Length")
ax.set_ylabel("Time to 4D Model Generation (seconds)")
ax.scatter(num_bins, times, color='aqua')
plt.savefig("Figures/Timing/timing_by_bin.png")


