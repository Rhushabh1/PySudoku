import numpy as np 


solved = [
	[4, 8, 6, 7, 5, 3, 2, 1, 9], 
	[5, 3, 7, 2, 1, 9, 8, 6, 4], 
	[2, 9, 1, 8, 6, 4, 7, 3, 5], 
	[6, 4, 2, 9, 7, 5, 1, 8, 3], 
	[3, 7, 5, 6, 8, 1, 9, 4, 2], 
	[9, 1, 8, 4, 3, 2, 5, 7, 6], 
	[8, 2, 3, 1, 9, 6, 4, 5, 7], 
	[7, 5, 4, 3, 2, 8, 6, 9, 1], 
	[1, 6, 9, 5, 4, 7, 3, 2, 8]
]


def row_verify(a):
	cp = np.copy(a)
	t = np.arange(1,10)
	x = cp.sort(axis=1)
	if (cp==t).all():
		return True
	else:
		return False


def box_modify(cp):
	a = np.copy(cp)
	t = a.reshape(-1,3)
	a1 = t[0::3].reshape(-1,9) # box 0, 3, 6
	a2 = t[1::3].reshape(-1,9) # box 1, 4, 7
	a3 = t[2::3].reshape(-1,9) # box 2, 5, 8
	p = np.append(a1,a2, axis=1)
	p = np.append(p,a3, axis=1).reshape(9,9)
	return p


def main_checker(board):
	a = np.array(board)

	r = row_verify(a)
	c = row_verify(a.transpose())
	b = row_verify(box_modify(a))

	if r and b and c:
		return True
	else:
		return False


