#!/usr/bin/env python3

import numpy as np
import argparse
import param_reader as pr

from numpy.core.defchararray import array
from numpy.core.fromnumeric import prod
"""
This script computes if the resolution set in the PARAMS file is sufficient for the scale of the tree
Date: 09-November-2021 Author: Igor Segrovets
# argument parser code adapted from wabbit-python-tools by Thomas Engels

https://www.euclideanspace.com/maths/geometry/elements/plane/lineOnPlane/index.htm
https://www.mathworks.com/matlabcentral/answers/543686-vector-projection-on-a-plane

"""


def vecMag(vector):
	return np.linalg.norm(vector)

def unitV(vector):
    v = vector
    return v / np.linalg.norm(v)

def angle(v, u):
    vdotu = np.inner(v,u)
    vmag = vecMag(v)
    umag = vecMag(u)
    return np.arccos(vdotu/(vmag*umag))

def computeStats(path_TREE, path_PARAMS):
    params = pr.params(path_PARAMS)
    meanflow_axis = params.u_mean_set
    scale_factor = params.fractal_tree_scaling
    area = 0
    volume = 0
    max_y = 0
    min_dim = [10e5,10e5] #r, l
    c = 2
    with open(path_TREE, 'r') as f: 
        for line in f:
            a = line.split(",")
            a = [el.replace('\n','').replace(' ','') for el in a] 
            
            for i, el in enumerate(a):
                try:
                    a[i] = float(el)
                except:
                    a[i] = 0
            x = np.array([a[0],a[3]])
            y = np.array([a[1],a[4]])
            z = np.array([a[2],a[5]])
            A = np.array([a[3]-a[0],a[4]-a[1],a[5]-a[2]])#defines tree branch vector
            B = np.array(meanflow_axis) #defines normal to the observation plane
            r = a[6]*scale_factor
            
            max_y = max(a[4],max_y)
            min_dim[0] = min(min_dim[0],a[6])
            min_dim[1] = min(min_dim[1],vecMag(A))
            #print(vecMag(a))

            temp = np.cross(A,B)/vecMag(B)
            AonBplane = np.cross(B,  temp) / vecMag(B) 
            #print(A,"->|", AonBplane,"|*2*",  a[6],"=", vecMag(AonBplane)*c*a[6])
            
            area += (vecMag(AonBplane*scale_factor)*c*a[6])*(scale_factor)

           # Bn = unitV(B)
           # An = unitV(A)
           # Bnn = np.inner(np.inner(Bn,An),Bn)
           # vn = An - Bnn
           # theta = angle(vn,An)
           # v = A*np.cos(theta)
            volume += (vecMag(A*scale_factor)*np.pi*(a[6]*scale_factor)**2.)
    return params, area, volume, max_y*scale_factor, [i*scale_factor for i in min_dim]


"""
TODO
import the params file
read the bloack size, refinemnt level and domain size to estimate is minimum feature is resolved

"""
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    #parser.add_argument("treeout",type=str,help="""tree-out.in file""")
    #parser.add_argument("params",type=str,help="""PARAMS.ini file""")
    parser.add_argument("-d","--directory",nargs='?',const='./',help="""
    					directory of files, if not ./""")
    args = parser.parse_args()

    if args.directory is None:
        # default is working directory
        dir = './'
    else:
        dir = args.directory

    if dir[-1] != '/':
        dir = dir+'/'

    tree_path = dir + "tree-out.in"
    path_params = dir + "PARAMS_tree.ini"

    try:
        params, tree_area, vol,  max_h, min_dims = computeStats(tree_path, path_params)
    except FileNotFoundError:
        print("ERROR: [files not found] Try specifying a valid directory with the -d flag")
    else:
        Ls = params.domain_size[0]
        Bs = params.number_block_nodes
        rl = params.max_treelevel
       
        dx_min = (2.0**(-rl))*Ls/Bs
        bsrec = (2**(-rl))*Ls/min(min_dims)
        print("total projected area.\t%.3f m^2"%tree_area)
        print(" \tour est. \t",vol,"m^3")
        print("\tmax height.\t %.3f m"%max_h)
        print("max resolution is \t%.5f,\nmin dimension is\t "%(dx_min),min_dims)
        print("Bs should be >=", bsrec, int(np.ceil(bsrec)))
        print("\n & %.i & %.i & %.3e & %.3e \\\\"%(Bs,rl,dx_min,min(min_dims)))

