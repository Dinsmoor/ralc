#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  townGen.py
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
#  responsible for making buildings, and doing logic for deciding how
#  many buildings there will be, will pass info to civGen, and then
#  use that data for populatng city

import random, bldgGen
from libdndGen import *

class Settlement(object):
	def __init__(self, techLevel, biome):
		self.techLevel = techLevel
		self.biome = biome
		self.citySize = self.getCitySize()
		self.s = self.getStreets()
		#neatDicPrint(self.s)


	def testdef(self, data):
		for li in data:
			neatListPrint(li)
			#neatDicPrint(li)
			#for li in di:
			#	neatListPrint(li)

	def getBldgData(self):
		return bldgGen.main('town',self.techLevel, self.biome)

	def getCitySize(self):
		# city size multipliers
		d ={
			'forest':1,
			'plains':0.7,
			'hills':0.7,
			'tundra':0.3,
			'marsh':0.4,
			'desert':0.2
			}
		return int(d[self.biome] * (random.randint(1,4) + 10))

	def getStreets(self):
		streets = {}
		for val in xrange(0,self.citySize):
			streets[getStreetName()] = self.fillStreet()
		#neatDicPrint(streets)
		return streets



	def fillStreet(self):
		lotCount = 2
		bldgList = []
		for lot in xrange(0,lotCount):
			bldgList.append(self.getBldgData())
		return bldgList

def main(opt, techLevel, biome):
	if opt == 'map':
		town = Settlement(techLevel, biome)
		return town.s
	else:
		return Settlement(1,'forest')
	return 0

if __name__ == '__main__':
	main(None,None,None)

