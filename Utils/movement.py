import pdb
import time
import cupy  as cp
import numpy as np

def movement(struc_t):
        loss = np.linalg.norm(struc_t[0:-1]-struc_t[1:])**2
        return loss

def movementLoss(struc_t):
        change = np.zeros(struc_t.shape)
        change[0:-1]  = struc_t[0:-1]-struc_t[1:]
        return change

def movementGPU(struc_t):
        loss = cp.linalg.norm(struc_t[0:-1]-struc_t[1:])**2
        return loss

def movementLossGPU(struc_t):
        change = cp.zeros(struc_t.shape)
        change[0:-1]  = struc_t[0:-1]-struc_t[1:]
        return change

