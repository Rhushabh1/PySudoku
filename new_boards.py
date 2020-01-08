import random
from checker import box_modify
import numpy as np 
from functools import reduce
from backtrack_solver import *


board = [
    [4,8,0,0,0,0,2,0,0],
    [5,3,7,2,1,0,0,0,4],
    [0,0,0,0,0,0,0,3,0],
    [0,0,2,0,7,0,1,0,3],
    [0,0,0,6,0,1,0,0,0],
    [9,0,8,0,3,0,5,0,0],
    [0,2,0,0,0,0,0,0,0],
    [7,0,0,0,2,8,6,9,1],
    [0,0,9,0,0,0,0,2,8]
]


def fill_band(board):
	t = np.arange(1,10)
	a = np.copy(board)

	# setting up 2nd box
	r1 = np.setdiff1d(t, a[0, :3])
	r1 = np.random.choice(r1, 3, replace=False)
	r2 = np.setdiff1d(a[2, :3], r1)
	r2 = np.append(r2, np.random.choice(a[0, :3], 3-r2.size, replace=False))
	r3 = reduce(np.setdiff1d, (t, r1, r2, a[2, :3]))
	b1 = reduce(np.append, (r1, r2, r3)).reshape(3, 3)
	np.apply_along_axis(np.random.shuffle, 1, b1)
	a[0:3, 3:6] = b1

	# setting up 3rd box
	b2 = reduce(np.append, (np.setdiff1d(t, a[0, :6]), np.setdiff1d(t, a[1, :6]), np.setdiff1d(t, a[2, :6]))).reshape(3, 3)
	np.apply_along_axis(np.random.shuffle, 1, b2)
	a[0:3, 6:9] = b2

	return a


def new_solution_grid():
	a = np.arange(1,10)
	np.random.shuffle(a)
	a = box_modify(np.append(a, np.zeros((8,9))).reshape(9,9))
	a = fill_band(a)
	b = fill_band(np.transpose(a))
	b = np.transpose(b)
	a[3::] = b[3::]
	solve(a)
	return a


def generate_new_puzzle():
	a = new_solution_grid()
	return a


def generate_hint():
	pass



