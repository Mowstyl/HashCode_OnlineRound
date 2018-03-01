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
'''

def sort_rides(rides):
	return np.sort(rides,key = ride_distance)

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
	fh.savePFile(output, sol)

def schedule():
    step = 0
