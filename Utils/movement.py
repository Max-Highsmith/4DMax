import time
import numpy as np

def movement(struc_t):
        loss = np.linalg.norm(struc_t[0:-1]-struc_t[1:])**2
        return loss

def movementLoss(struc_t):
        start = time.time()
        change = np.zeros(struc_t.shape)
        change[0:-1]  = struc_t[0:-1]-struc_t[1:]
        #print("move time:",time.time()-start)
        return change

