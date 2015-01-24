#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  libdndGen.py
#
#  Copyright 2014 Tyler Dinsmoor <d@d-netbook>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#



def getFromFile_LoL(fi):
	fi = open(fi)
	# Builds a list of lists from a file, seperated by newline
	li = [i.strip().split(',') for i in fi.readlines() if not i.startswith("#")]
	# ignore blank lines
	li = [x for x in li if x != ['']]
	li = [[st.strip() for st in l] for l in li]
	fi.close()
	return li

def getFromFile_Dic(fi):
	d = {}
	with open(fi) as f:
		for line in f:
			if not line.startswith("#"):
				(key, val) = line.strip().split('=')
				d[key] = val
	return d

def getFromFile_T(fi):
	fi = open(fi)
	li = [i.strip().split('\n') for i in fi if not i.startswith("#")]
	li = [x for x in li if x != ['']]
	tu = tuple(li)
	fi.close()
	return tu


def maxi(l):
	m = max(l)
	for i, v in enumerate(l):
		if m == v:
			return i
def mini(l):
	m = min(l)
	for i, v in enumerate(l):
		if m == v:
			return i
def wChoice(wCh):
	import random
	'''must be in format: wChoice(('a',1.0),('b',2.0),('c',3.0))'''
	totalChoice = sum(w for c, w in wCh)
	random_uniform = random.uniform(0, totalChoice)
	upto = 0
	for c, w in wCh:
		if upto + w > random_uniform:
			return c
		upto += w
	assert False, "Shouldn't get here"

def neatListPrint(l):
	for i in l:
		print "\t",i

def neatDicPrint(d):
	for key,val in d.iteritems():
		print "\t%s\t%s"%(key, val)

def gridDistance(points):
	import math
	p0, p1 = points
	return int(math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2))

def getCityName():
	import random
	cityname = random.choice(getFromFile_T('data/cities'))
	for s in cityname:
		return s
def getVillageName():
	import random
	villageName = random.choice(getFromFile_T('data/villages'))
	for s in villageName:
		return s
def getCampName():
	import random
	campName = random.choice(getFromFile_T('data/camps'))
	for s in campName:
		return s
def getBldgName():
	import random
	bldgName = random.choice(getFromFile_T('data/bldgs'))
	for s in bldgName:
		return s
def getStreetName():
	import random
	streetName = random.choice(getFromFile_T('data/streets'))
	for s in streetName:
		return s
