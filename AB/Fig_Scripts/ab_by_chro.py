import numpy as np
import matplotlib.pyplot as plt

chros = [1,2,3,4,5,6,7,8,9,10,11,12,13,15,16,17,18,19]
fig, ax = plt.subplots(len(chros))
for c, chro in enumerate(chros):
	abvec = np.load("AB_Vecs/real_ipsc_day_ES_rep_1_chro_"+str(chro)+".npy")
	ax[c].bar(list(range(0, len(abvec))), abvec)

plt.show()
