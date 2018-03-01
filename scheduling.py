#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math as m
import numpy as np
import filehandler as fh

# Mannhatan distance between two points
def man_distance(c1,c2):
	return math.abs(c1[0] - c2[0]) + math.abs(c1[1] - c2[2])

# Ride distance between start and finish for a ride
def ride_distance(ride):
	return man_distance(ride[0],ride[1])

'''ride:
    (a,b),
    (c,d),
    start,
    finish
	id
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
    if(kwargs['mode']=='0'):
        k = lambda ride: ride[2]
    elif (kwargs['mode']=='1'):
		k = ride_distance
	else:
        k = lambda ride: ride[3]

	return sorted(rides, key = k)

def main(argv): # We expect to receive input file as first argument and output file second argument (optional). If output not specified, defaults to input+.out
	if len(argv) < 1:
		print("Input file location expected. Output file can be also specified (optional)")
		return
	input = argv[0]
	output = input + ".out"
	#maxLevel = 5
	#maxSlices = 50
	#if len(argv) > 1:
	#	output = argv[1]
	#try:
	#	if len(argv) > 2:
	#		maxLevel = int(argv[2])
	#except:
	#	print("maxLevel must be an integer. Default to maxLevel=5")
	#	maxLevel = 5
	#try:
	#	if len(argv) > 3:
	#		maxSlices = int(argv[3])
	#except:
	#	print("maxSlices must be an integer. Default to maxSlices=50")
	#	maxSlices = 50
	try:
		map_info, rides = fh.loadRFile(input)
	except Exception as e:
		print (str(e))
		print ("Program ended with errors!")
		return
	#start = timer()
	sol = schedule(map_info, rides)
	#end = timer()
	#print("\nTime elapsed: %.4f seconds." % round(end-start, 4))
	#print (str(sol[0]) + " slices")
	#print (sol[1])
	#print ("Score: " + str(sol[2]) + "/" + str(c*r))
	global exploredNodes
	print ("Explored Nodes: " + str(exploredNodes))
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
    step = 0
    orides = sort_rides(rides, mode=2)
    freev = [[i, (0, 0), None] for i in range(map_info[2])] # Lista de vehiculos con su id, posicion y su ride asignado
    workv = [] # Lista de vehiculos trabajando
    donejob = {} # Diccionario que indiza por id de vehiculo y que almacena listas de trabajos completados
    mapsim = np.zeros((map_info[0], map_info[1]))
    mapsim[0,0] = map_info[2]
    currentrides = []

    while true:
        ridestodel = []
        for i in range(len(orides)):
            if len(freev) > 0:
                freev.sort(key = lambda v: man_distance(v[1], orides[i][0]))
                endtime = man_distance(freev[0][1], orides[i][0]) +


if __name__ == "__main__":
	main(sys.argv[1:])
