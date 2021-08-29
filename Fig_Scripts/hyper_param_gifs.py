import numpy as np
import matplotlib.pyplot as plt
import glob
import os

np_4ds = glob.glob("Generated_Structures/tuning*epoch_100_*")
for np_4d in np_4ds:
    folder="Gifs/hyper_param/"+np_4d.split("/")[1].split(".npy")[0]
    command = "python Python_Scripts/create_gif.py "+str(folder)+" "+str(np_4d)
    print(command)
    os.system(command)

