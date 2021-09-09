import sys
sys.path.append("..")
sys.path.append(".")
sys.path.append("Utils")
import pdb
import numpy as np
import matplotlib.pyplot as plt
import tads as tt

#exp parameters
#CHROS  = np.arange(1,20) 
CHROS = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,'X']
REPS   = [1,2]

#missing times
MISS   = [2,4,6,8]
GRAN   = [4,8,12,16]

#time on 4d model to sample from
DAYS  = np.array(['B','D2','D4','D6','D8','ES'])

real_TAD = {}
#get tad predictions from real Hi-C dataa
for chro in CHROS:
    for day in DAYS:
        for rep in REPS:
            real_contact_data_STR = "".join(["HiC_Tool_Tads",
                    "/tad_real_ipsc_day_",
                    str(day),
                    "_rep_"+str(rep),
                    "_chro_"+str(chro),
                    ".npy"])
            real_TAD[chro, rep, day] = np.load(real_contact_data_STR)


recon_tads = {}
for rep in REPS:
    for chro in CHROS:
        for gran in GRAN:
            loadstr      = "".join(["HiC_Tool_Tads",
                            "/ipscFull",
                            "_"+str(rep),
                            "_1000_0.6_0.0001_400_50000_21_",
                            str(chro)+".npy"])
            temp      = np.load(loadstr,
                            allow_pickle=True,
                            encoding='bytes')
            recon_tads[chro, gran, rep] = temp.item()
	



#get Tad predictions from structure
colors = ['blue', 'red', 'orange','yellow']
inter_tads = {}

for rep in REPS:
    for chro in CHROS:
        for mis in MISS:
            loadstr      = "".join(["HiC_Tool_Tads",
                            "/ipsc_"+str(mis),
                            "_"+str(rep),
                            "_1000_0.6_0.0001_400_50000_21_",
                            str(chro)+".npy"])
            temp      = np.load(loadstr,
                            allow_pickle=True,
                            encoding='bytes')
            inter_tads[chro, mis,rep] = temp.item()
	
bar = np.zeros((len(CHROS), 4, 5))
compfunc = tt.getPercentOverlap



for c, chro in enumerate(CHROS):
    for t, (day, indx, mis) in enumerate(
            zip(['D2', 'D4', 'D6','D8'],
                [4,8,12,16],
                MISS)):
        print(str(day),",",str(indx))
        base = real_TAD[chro, 1, day] 
        REPLICATE = bar[c, t, 0] = compfunc(real_TAD[chro, 2, day], base)
        RECON_1 = bar[c, t, 1]  = compfunc(recon_tads[chro, gran, 1][indx], base)
        INTERP_1 = bar[c, t, 2]  = compfunc(inter_tads[chro, mis,1][indx], base)
        RECON_2 = bar[c, t, 3]  = compfunc(recon_tads[chro, gran, 2][indx], base)
        INTERP_2 = bar[c, t, 4]  = compfunc(inter_tads[chro, mis,2][indx], base)

'''
fig, ax = plt.subplots(6,5)
for c, chro in enumerate(CHROS):
	ax[int(c%6), int(c/6)].imshow(bar[c],
                cmap="Greens",
                vmin=0.4,
                vmax=1)#, vmin=0, vmax=1)
	for (j, i), label in np.ndenumerate(bar[c]):
		ax[int(c%6),int(c/6)].text(i,j, 
                        "{0:0.2f}".format(bar[c,j,i]),
                            ha='center',
                            va='center',
                            fontsize=4,
                            color="white")
		ax[int(c%6),int(c/6)].set_ylabel("Chro "+str(chro))
		ax[int(c%6),int(c/6)].set_yticklabels(["D2","D4","D6","D8"])
		ax[int(c%6),int(c/6)].set_yticks([0,1,2,3])
		ax[int(c%6),int(c/6)].set_xticks([])

ax[5,3].set_xticklabels(["HiC Rep", 
                        "4D Recon 1",
                        "4D Interp 1",
                        "4D Recon 2",
                        "4D Interp 2"])
ax[5,3].set_xticks([0,1,2,3,4])
plt.xticks(rotation=90)
plt.savefig("test.svg")
plt.show()
'''

for c, chro in enumerate(CHROS):
    fig, ax = plt.subplots(figsize=(1,1))
    ax.imshow(bar[c],
            cmap="Greens",
            vmin=0.4,
            vmax=1)
    for (j, i), label in np.ndenumerate(bar[c]):
        ax.text(i,j,
                "{0:0.2f}".format(bar[c,j,i]),
                ha='center',
                va='center',
                fontsize=4,
                color="white")
        ax.set_yticks([])
        ax.set_xticks([])
    plt.savefig(str(chro)+".png", dpi=200)



