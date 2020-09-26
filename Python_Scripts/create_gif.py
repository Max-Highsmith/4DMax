from scipy import stats
import os
import pdb
import sys
import numpy as np
import matplotlib.pyplot as plt

def altPlot3d(struc, dirr):
        maxx =0.
        minn =0.
        def clean(x,y,z):
                x_score = np.abs(stats.zscore(x))
                y_score = np.abs(stats.zscore(y))
                z_score = np.abs(stats.zscore(z))
                threshold = 3
                toRemove = np.hstack((np.where(x_score>3), np.where(y_score>3), np.where(z_score>3)))
                toRemove = np.unique(toRemove)
                xclean   = np.delete(x,toRemove)
                yclean   = np.delete(y,toRemove)
                zclean   = np.delete(z,toRemove)	
                return xclean, yclean, zclean

        for t in range(0, struc.shape[0]):
                x = struc[t][:,0]
                y = struc[t][:,1]
                z = struc[t][:,2]
                '''
                x_score = np.abs(stats.zscore(x))
                y_score = np.abs(stats.zscore(y))
                z_score = np.abs(stats.zscore(z))
                threshold = 3
                toRemove = np.hstack((np.where(x_score>3), np.where(y_score>3), np.where(z_score>3)))
                toRemove = np.unique(toRemove)
                xclean   = np.delete(x,toRemove)
                yclean   = np.delete(y,toRemove)
                zclean   = np.delete(z,toRemove)
                '''
                xclean, yclean, zclean = clean(x,y,z)
                maxx=np.max((xclean,yclean,zclean,np.repeat(maxx, xclean.shape[0])))
                minn=np.min((xclean,yclean,zclean,np.repeat(minn, xclean.shape[0])))
                window = (minn, maxx)

        for t in range(0,struc.shape[0]):
                plt.close()
                plt.clf()
                fig = plt.figure()
                ax  = plt.axes(projection="3d")
                fig.set_size_inches(14,10)
                x   = struc[t][:,0]
                y   = struc[t][:,1]
                z   = struc[t][:,2]
                x,y,z = clean(x,y,z)
                ax.plot(x,y,z, linewidth=1)
                ax.set_title(str(t))
                ax.set_xlim(window[0], window[1])
                ax.set_ylim(window[0], window[1])
                ax.set_zlim(window[0], window[1])
                #for i in range(0,x.shape[0]):
                #       ax.text(x[i],y[i],z[i], s=str(i))
                plt.savefig(dirr+"/"+str(t)+".png")


def plot3d(struc, dirr):
        maxx =0.
        minn =0.
        for t in range(0, struc.shape[0]):
                x = struc[t][:,0]
                y = struc[t][:,1]
                z = struc[t][:,2]
                maxx=np.max((x,y,z,np.repeat(maxx, x.shape[0])))
                minn=np.min((x,y,z,np.repeat(minn, x.shape[0])))
                window = (minn, maxx)
        for t in range(0,struc.shape[0]):
                plt.close()
                plt.clf()
                fig = plt.figure()
                ax  = plt.axes(projection="3d")
                fig.set_size_inches(14,10)
                x   = struc[t][:,0]
                y   = struc[t][:,1]
                z   = struc[t][:,2]
                ax.plot(x,y,z, linewidth=1)
                ax.set_title(str(t))
                ax.set_xlim(window[0], window[1])
                ax.set_ylim(window[0], window[1])
                ax.set_zlim(window[0], window[1])
                #for i in range(0,x.shape[0]):
                #       ax.text(x[i],y[i],z[i], s=str(i))
                plt.savefig(dirr+"/"+str(t)+".png")

OUT_DIR    = sys.argv[1].split(".gif")[0]
if not os.path.exists(OUT_DIR):
	os.mkdir(OUT_DIR)
STRUC_FILE = sys.argv[2]
structure  = np.load(STRUC_FILE)
altPlot3d(structure, OUT_DIR)
numImages = str(structure.shape[0]-1)
os.system("./make_real_gif.sh "+str(numImages)+" "+str(OUT_DIR)+" "+OUT_DIR+".gif")
