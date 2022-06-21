#!/usr/bin/env python3
import numpy as np
import argparse

cd = [[4.00946e+1, 1.61427e+0],
[9.26747e+1, 1.32058e+0],
[2.07823e+2, 1.08010e+0],
[4.16603e+2, 8.92949e-1],
[1.01816e+3, 7.40941e-1],
[3.40778e+3, 6.59335e-1],
[1.69603e+4, 6.56864e-1],
[6.71167e+4, 6.54747e-1],
[1.13159e+5, 6.18500e-1],
[1.75206e+5, 5.11498e-1],
[2.04761e+5, 3.42903e-1],
[2.20580e+5, 1.83295e-1],
[2.85526e+5, 9.87208e-2],
[4.16292e+5, 1.07001e-1],
[6.49515e+5, 1.63911e-1],
[1.13813e+6, 2.51656e-1],
[2.43142e+6, 3.74538e-1],
[5.34945e+6, 4.26489e-1],
[1.10187e+7, 4.69680e-1],
[3.58993e+7, 5.12166e-1]]

cdx = [cd[i][0] for i in range(len(cd))]
cdy = [cd[i][1] for i in range(len(cd))]

def sphereCD(re):
	return np.interp(re,cdx,cdy)

def sphereDrag(re, L):
	CD = np.interp(re,cdx,cdy)
	return CD * .5 *  np.pi * (L/2.)**2


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("re",type=float,help="""
    			reynolds number\n""")
	parser.add_argument("L",type=float,help="""
    			length\n""")
	args = parser.parse_args()

	Re = args.re
	L = args.L

	D =sphereDrag(Re, L)
	CD =sphereCD(Re)
    
	print('\ntheoretical F_D from Re around 3d sphere \t:::: %.3f'%D)
	print('theoretical Cd around a 3D sphere \t\t:::: %.3f '%CD)


