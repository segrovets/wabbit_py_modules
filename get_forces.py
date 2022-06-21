#!/usr/bin/env python3

import matplotlib.pyplot as plt
import argparse


def getForces(path):
    xf = []
    with open(path, newline = '\n') as f:
        for row in f:
            columns = row.split(' ')
            columns = [float(dat.strip()) for dat in columns if (dat != '')]
            xf.append(columns)  
    return xf


def getDissF(path):
    xf = []
    with open(path, newline = '\n') as f:
            for row in f:
                columns = row.split(' ')
                columns = columns[7:]
                columns = [float(dat.strip()) for dat in columns if (dat != '')]
                xf.append(columns) 
                #print(xf[-1]) 
    return xf[-1]


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("forcefile",type=str,help="""
    			forces.t file produced by wabbit\n""")
    parser.add_argument("-d","--directory",nargs='?',const='./',help="""
    					directory of tree files, if not ./""")

    args = parser.parse_args()

    def checkDir(param):
        if param is None:
            # default is working directory
            dir = './'
        else:
            dir = param

        if dir[-1] != '/':
            dir = dir+'/'
        return dir

    dir = checkDir(args.directory)
    file_path = dir + args.forcefile

    forces = getForces(file_path)
    print(forces)