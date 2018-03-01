#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Formats for loading:
ride:
    (a,b),
    (c,d),
    start,
    finish
    id
    usable
map:
	rows,
	cols,
	vehics,
	rides,
	bonus,
	steps

returns:
    (mapdata, [ride1, ..., rideN])

Formats for saving:
listvec:
    ridesassigned (list)
'''
def loadRFile(filename):
	inputfile = open(filename, "r")
	if inputfile == None:
		raise ValueError("File not found!")
	first = inputfile.readline().split()
	if len(first) != 6:
		raise ValueError('Bad formatted file! First line must contain "ROWS,COLUMNS,VEHICLES,RIDES,BONUSES,STEPS"')
	try:
		r, c, f, n, b, t = [int(x) for x in first]
		if r < 1 or r > 10000 or c < 1 or c > 10000 or f < 1 or f > 1000 or n < 1 or n > 10000 or b < 1 or b > 10000 or t < 1 or t > pow(10,9):
			raise ValueError('Invalid range for either ROWS, COLUMNS, VEHICLES, RIDES, BONUSES or STEPS')
	except:
		raise ValueError('ROWS,COLUMNS,VEHICLES,RIDES,BONUSES,STEPS must be integers!')

	mapdata = (r, c, f, n, b, t)
	rides = []
	for i in range(n):
		line = inputfile.readline()
		if line == None:
			raise ValueError("Invalid number of rows! Expected " + str(r))
		line = line.split()
		if len(line) != 6:
			raise ValueError("Invalid number of values! Expected 6 " + " Found " + str(len(line)))
		ride = []
		try:
			a, b, x, y, s, f = [int(x) for x in line]
		except:
			raise ValueError("Expected Rides Format: START ROW, START COLUMN, END ROW, END COLUMN, EARLIEST START and LATEST FINISH must be integers!")
		if a < 0 or a >= r or x < 0 or x >= r:
			raise ValueError("Start row and end row must be within 0 and ROWS (not included)")
		if b < 0 or b >= c or y < 0 or y >= c:
			raise ValueError("Start column and end column must be within 0 and COLUMNS (not included)")
		if s < 0 or s >= t:
			raise ValueError("Earliest start must be within 0 and STEPS (not included)")
		if f < 0 or f > t:
			raise ValueError("The latest finish must be between 0 and the number of steps")

		ride = [(a,b),(x,y),s,f,i,True]
		rides.append(ride)

	return (mapdata, rides)

def saveRFile(filename, sol):
	f = open(filename, "w+")
	for v in sol:
		f.write(str(len(v))+' ')
		for i in v:
			f.write(str(i) + ' ')
		f.write('\n')
