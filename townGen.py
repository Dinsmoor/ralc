#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  townGen.py
#
#  Copyright 2014 Tyler Dinsmoor <pappad@airmail.cc>
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
#  responsible for making buildings, and doing logic for deciding how
#  many buildings there will be, will pass info to civGen, and then
#  use that data for populatng city
try:
	import random
	import bldgGen
except ImportError:
	print "You are missing essential Libraries. See README.md"
	exit()

def getFromFile_T(fi):
	fi = open(fi)
	li = [i.strip().split('\n') for i in fi if not i.startswith("#")]
	li = [x for x in li if x != ['']]
	tu = tuple(li)
	fi.close()
	return tu

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
def getStreetName():
	import random
	streetName = random.choice(getFromFile_T('data/streets'))
	for s in streetName:
		return s

class Settlement(object):
	def __init__(self, biome, pref):
		self.settings = pref
		citySize = self.getCitySize(biome)
		self.s = self.getStreets(citySize, biome)

	def getBldgData(self, biome):
		return bldgGen.main('town', biome, self.settings)

	def getCitySize(self, biome):
		# city size multipliers
		size_mult ={
			'forest':1,
			'plains':0.7,
			'hills':0.7,
			'tundra':0.3,
			'marsh':0.5,
			'desert':0.2,
			'small':0.2,
			}


		return int(size_mult[biome] * (random.randint(1,4) + 10))

	def getStreets(self, citySize, biome):
		streets = dict()
		for val in xrange(0,citySize):
			streets[getStreetName()] = self.fillStreet(biome, citySize)
		return streets

	def fillStreet(self, biome, citySize):
		lotCount = random.randint(1,4) + citySize
		bldgList = []
		for lot in xrange(0,lotCount):
			bldgList.append(self.getBldgData(biome))
		return bldgList

def main(opt, biome, pref):
	if opt == 'big':
		town = Settlement(biome, pref)
		return town.s
	if opt == 'small':
		town = Settlement('small', pref)
		return town.s
	else:
		town = Settlement('forest', pref)
		return 0

if __name__ == '__main__':
	main(None,None, dict())

