import numpy as np
import pdb
import glob
def loadClusterTAD(fn):
	bestCluster = glob.glob("Cluster_Tads/"+fn+"/TADs/Be*")
	tads        = np.loadtxt(bestCluster[0],str, skiprows=1)
	
	x = np.loadtxt(fn)
	return x[:,(1,3)].astype(int)

def getTadSetSim(tadSet1, tadSet2):
    THRESHOLD = 150000
    nearests = []
    within   = []
    for interval1 in tadSet1:
        nearest = 10000000000000
        for interval2 in tadSet2:
            dist = min(np.abs(interval1[1] - interval2[1]), 
                    np.abs(interval1[0] - interval2[0]))
            if dist < nearest:
                nearest = dist
        nearests.append(nearest)
        if nearest <= THRESHOLD:
            within.append(1)
        else:
            within.append(0)
    return nearests, np.array(within)

def getPercentOverlap(tadSet1, tadSet2):
    nearests, within = getTadSetSim(tadSet1, tadSet2)
    return np.sum(within == 1) /tadSet1.shape[0]

