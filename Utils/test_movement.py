import time
import pdb
import numpy as np
import cupy  as cp
import pytest
import util as ut
import movement as mv
def test_movement():
	struc          = np.load("Utils/test_data/test_struc.npy")
	real_movement  = np.load("Utils/test_data/test_movement.npy")
	start_time     = time.time()
	pass_movement  = mv.movement(struc)
	print("test_movement", str(time.time()-start_time))
	assert((pass_movement - real_movement)<1e-10)

def test_movementLoss():
	struc              = np.load("Utils/test_data/test_struc.npy")
	real_movement_loss = np.load("Utils/test_data/test_movement_loss.npy")
	start_time     = time.time()
	pass_movement_loss = mv.movementLoss(struc)
	print("test_movementLoss", str(time.time()-start_time))
	assert(((pass_movement_loss - real_movement_loss)<1e-10).all())

def test_movementGPU():
	struc          = cp.load("Utils/test_data/test_struc.npy")
	real_movement  = cp.load("Utils/test_data/test_movement.npy")
	start_time     = time.time()
	pass_movement  = mv.movementGPU(struc)
	print("test_movementGPU", str(time.time()-start_time))
	assert((pass_movement - real_movement)<1e-10)

def test_movementLossGPU():
	struc              = cp.load("Utils/test_data/test_struc.npy")
	real_movement_loss = cp.load("Utils/test_data/test_movement_loss.npy")
	start_time     = time.time()
	pass_movement_loss = mv.movementLossGPU(struc)
	print("test_movementLossGPU", str(time.time()-start_time))
	assert(((pass_movement_loss - real_movement_loss)<1e-10).all())

