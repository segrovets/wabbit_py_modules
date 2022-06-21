#!/usr/bin/env python3

import numpy as np
import re

class params():
    def __init__(self, path):
        with open(path, 'r') as f:
            print("reading file..",path)
            for line in f:
                line = line.strip()
                if len(line) == 0: continue
                if (line[0] == ';')or(line[0] == '['): continue
                if (line.count('='))>0:
                    line = line[0:line.find(';')]
                columns = re.split(" |=|,",line)
                name = columns[0]
                value = columns[1:]
                try:
                    value = [int(val) for val in value]
                except:
                    try:
                        value = [float(val) for val in value]
                    except:
                        continue
                if len(value)==1:
                    value = value[0]
                setattr(self,name,value)
                


