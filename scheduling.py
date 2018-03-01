#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math as m
#import numpy as np
import filehandler as fh
import sys

# Mannhatan distance between two points
def man_distance(c1,c2):
    return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])

# Ride distance between start and finish for a ride
def ride_distance(ride):
    return man_distance(ride[0],ride[1])

'''ride:
    (a,b),
    (c,d),
    start,
    finish,
    id,
    usable
'''

def sort_rides(rides, **kwargs): # kwargs['mode']: 0 -> ordenar por start, 1 -> ordenar por ride_distance
# 2 -> finish
    '''
    # En caso de emergencias
    if(kwargs):
            l_ord = []
            if(kwargs['mode']=='0'):
                for i in rides:
                    l_ord.append((i[5],i[2]))
                    l_ord.sort(key=lambda x: x[1])
                    return [i[0] for i in l_ord]

            elif (kwargs['mode']=='1'):
                for i in rides:
                    l_ord.append((i[5],ride_distance(i[0],i[1])))
                    l_ord.sort(key=lambda x: x[1])
                    return [i[0] for i in l_ord]
            else:
                for i in rides:
                    l_ord.append((i[5],i[3])
                    l_ord.sort(key=lambda x: x[1])
                    return [i[0] for i in l_ord]

    '''
    rev = False
    if(kwargs['mode']=='0'):
        k = lambda ride: ride[2]
    elif (kwargs['mode']=='1'):
        k = ride_distance
        rev = True
    else:
        k = lambda ride: ride[3]

    return sorted(rides, key = k, reverse = rev)

def main(argv): # We expect to receive input file as first argument and output file second argument (optional). If output not specified, defaults to input+.out
    if len(argv) < 1:
        print("Input file location expected. Output file can be also specified (optional)")
        return
    input = argv[0]
    output = input + ".out"
    try:
        map_info, rides = fh.loadRFile(input)
    except Exception as e:
        print (str(e))
        print ("Program ended with errors!")
        return
    sol = schedule(map_info, rides)
    fh.saveRFile(output, sol)

'''
map:
    rows,      0
    cols,      1
    vehics,    2
    rides,     3
    bonus,     4
    steps      5
'''
def schedule(map_info, rides):
    step = 1
    orides = sort_rides(rides, mode=1)
    freev = [[i, (0, 0), None, None] for i in range(map_info[2])] # Lista de vehiculos con su id, posicion y su ride asignado, asi como el tiempo en el que volvera a ser libre (willy)
    donejob = [[] for i in range(map_info[2])] # Diccionario que indiza por id de vehiculo y que almacena listas de trabajos completados
    maxstep = max([ride[3] for ride in orides])
    #print (maxstep)

    while step <= maxstep and any([ride[5] for ride in orides]):
        #print ("Step: " + str(step))
        #print ("Working v: " + str(len(workv)) + " with rides " + str([v[2][4] for v in workv]))
        for i in range(len(freev)):
            if step == freev[i][3]:
                print("Ride " + str(freev[i][2][4]) + " finished!")
                freev[i][1] = freev[i][2][1]
                freev[i][2] = None
                freev[i][3] = None
        for i in range(len(orides)):
            if orides[i][5]: # any([v[2] is not None for v in freev])
                freev.sort(key = lambda veh: man_distance(veh[1], orides[i][0]) if veh[2] is None else sys.maxsize)
                #print(str(freev[0]))
                if freev[0][2] is None:
                    delay = orides[i][2] - (step + man_distance(freev[0][1], orides[i][0]))
                    if delay < 0:
                        delay = 0
                    endtime = step + man_distance(freev[0][1], orides[i][0]) + delay + ride_distance(orides[i])
                    if endtime <= orides[i][3]:
                        freev[0][2] = orides[i]
                        freev[0][3] = endtime
                        #print(str("Ride " + str(orides[i][4]) + " assigned to car " + str(freev[0][0])))
                        donejob[freev[0][0]].append(orides[i][4])
                    orides[i][5] = False
                else:
                    #print("No free cars!")
                    break
        step += min([v[3]-step if v[3] is not None else 1 for v in freev])

    return [v for v in donejob]

if __name__ == "__main__":
    main(sys.argv[1:])
