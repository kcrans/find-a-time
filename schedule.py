import numpy as np
from z3 import *
import re
import sys

a = []
with open('whenisgood.txt') as f:
    read_data = f.read()
    p = re.compile(r'\.name = ".+"')
    names = p.findall(read_data)
    justnames = list(map(lambda x : x[9:-1], names))
    #print(justnames)
    p = re.compile(f'myCanDos = "[,\d]+"')
    candos = p.findall(read_data)
    justtimes = list(map(lambda x :(x[12:-1]).split(","), candos))
    finaltimes = [[int(time) for time in person] for person in justtimes]
    uniqtimes = sorted(set([item for sublist in finaltimes for item in sublist]))
    i = len(justnames)
    j = len(uniqtimes)
    #print(i, j)
    convert = {uniqtimes[i] : i for i in range(j)}
    #print(convert)
    data = np.zeros((i, j))
    for row, person in enumerate(finaltimes):
        for time in person:
            data[row, convert[time]] = 1
    a = data

def check(k, h):
    slots = [If(Bool(f"k{x}"), IntVal(1), IntVal(0)) for x in range(len(a[0]))]
    s = Solver()
    s.add(Sum(slots) == IntVal(k))
    for row in range(len(a)):
        options = []
        for time in range(len(a[0])):
            if a[row][time] == 1:
                options.append(slots[time])
        s.add(Sum(options) >= IntVal(h))
    print(s.check())
    try:
        print(s.model())
        return True
    except Z3Exception:
        return False

check(sys.argv[1], sys.argv[2])


