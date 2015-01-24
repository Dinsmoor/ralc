#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  bldgGen.py
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
# gets information provided from landGen to decide building construction
# passes info to townGen, which then makes a lot of buildings

'''
Needs to return a working desc of a building, how many rooms, how many
floors, materials, utilities, type of building(tavern, shop), how many
residents.
'''

from libdndGen import *
import charGen, random

'''
Building need:
	Rooms
	Inhabitants
	Descriptions:
		interior
		exterior
		affluence
	floors
	purpose
	efficency

'''


biome = 'forest'

class Building(object):
	'''
	Building needs walls, height, max inhabitatants, purpose
	'''
	def __init__(self,techLevel, biome):
		self.bldgDat = {}
		self.bldgDat['Purpose'] = self.getPurpose()
		self.bldgDat['Floors'] = 1
		(self.bldgDat['Roof'],self.bldgDat['Walls'],
			self.bldgDat['Floor']) = self.getBldgMake()
		self.bldgDat['Rooms'] = []
		self.bldgDat['Rooms'].append(self.getRooms(2))


	def getPurpose(self):
		bldgtypes = ('Shack','Residence','General Store',
					'Armorer','Courtyard',
					'Weapon Smith', 'Tavern', 'Inn')
		return random.choice(bldgtypes)

	def getRooms(self, rooms):
		roomDat = {}
		roomTypes = ('Entry','Kitchen','Living Area','Dining Area',
				'Common Area', 'Sleeping Quarters')
		count = 0
		for room in xrange(0,rooms):
			roomDat['roomID'] = count
			roomDat['Type'] = random.choice(roomTypes)
			roomDat['Actors'] = self.getInhabitants(2)
			count += 1
		return roomDat

	def getInhabitants(self, popul):
		inhabitantList = []
		for inhabitant in xrange(0,popul):
			personType = random.choice(('Commoner', 'Merchant',
							'Storekeeper', 'Peasant', 'Noble'))
			inhabitantList.append(charGen.main())
		return inhabitantList

	def getBldgMake(self):
		d = {
		#techlevel:roofing[0],walls[1],floor[2]
		1:(('thatch','straw'),('stick','mud'),('dirt','straw')),
		2:(('wooden','shingle'),('boarded','log','stone'),
			('wooden','stone')),
		3:(('sheet metal','shingle'),('concrete','stone','metal'),
			('wooden','metal','tile'))
		}
		materialsTup = d[1]
		return (random.choice(materialsTup[0]),
			random.choice(materialsTup[1]),
			random.choice(materialsTup[2]))

class Room(Building):
	def __init__(self):
		pass

def main(opt, techLevel, biome):
	'''
	This function is only kept until this program is capable of running
	indepentantly and will be removed after the program being debugged.
	'''

	if opt == 'town':
		bldg = Building(techLevel, biome)
		room = Room()
		return bldg.bldgDat
	else:
		bldg = Building(1,'forest')
		neatDicPrint(bldg.bldgDat)
		return 0

if __name__ == '__main__':
	main(None,None,None)

