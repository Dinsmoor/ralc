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
		self.bldgDat['Floors'] = random.randint(1,2)
		self.bldgDat['Rooms'] = {}
		self.bldgDat['Rooms'] = (self.getRooms(random.randint(1,3)))
		#self.testdef(self.bldgDat['Rooms'])

	def testdef(self, data):
		for li in data:
			for di in li:
				neatDicPrint(di)

	def getPurpose(self):
		bldgtypes = ('Shack','Residence','General Store',
					'Armorer','Livestock Area',
					'Weapon Smith', 'Tavern', 'Inn')
		return random.choice(bldgtypes)

	def getRooms(self, rooms):
		d = {
			'Shack':('Entry','Kitchen','Common Area'),
			'Residence':('Entry','Kitchen','Living Area','Dining Area',
				'Common Area', 'Sleeping Quarters'),
			'General Store':('Entry','Store Room'),
			'Armorer':('Entry','Forge'),
			'Livestock Area':('Entry','Barn','Slaughter Room'),
			'Weapon Smith':('Entry','Forge'),
			'Tavern':('Entry','Kitchen','Dining Area'),
			'Inn':('Entry','Kitchen',
				'Common Area', 'Sleeping Quarters')
			}

		roomTypes = d[self.bldgDat['Purpose']]

		roomDat = [{'Type':random.choice(roomTypes),
			'Actors':self.getInhabitants(random.randint(0,3))} for k in xrange(0,rooms)]
		return roomDat

	def getInhabitants(self, popul):
		inhabitants = {}
		for inhabitant in xrange(0,popul):
			personType = random.choice(('Commoner', 'Merchant',
							'Storekeeper', 'Peasant', 'Noble'))
			person = charGen.main()
			key_name = person['Name']
			inhabitants[key_name] = person
		return inhabitants

def main(opt, techLevel, biome):
	'''
	This function is only kept until this program is capable of running
	indepentantly and will be removed after the program being debugged.
	'''

	if opt == 'town':
		bldg = Building(techLevel, biome)
		return bldg.bldgDat
	else:
		bldg = Building(1,'forest')
		#print bldg.bldgDat
		neatDicPrint(bldg.bldgDat)
		return 0

if __name__ == '__main__':
	main(None,None,None)

