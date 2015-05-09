#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  bldgGen.py
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
# gets information provided from landGen to decide building construction
# passes info to townGen, which then makes a lot of buildings

try:
	import random
	import charGen
	from libdndGen import *
except ImportError:
	print "You are missing essential Libraries. See README.md"

class Building(object):
	'''
	Facilitates the population of itself, passes data to townGen
	'''
	def __init__(self, biome):
		self.bldgDat = {}
		self.bldgDat['Rooms'] = {}
		self.bldgDat['Purpose'] = self.get_purpose()
		self.bldgDat['Rooms'] = self.get_rooms(random.randint(1,3))

	def get_purpose(self):
		bldgtypes = ('Shack','Residence','General Store',
					'Armorer','Livestock Area',
					'Weapon Smith', 'Tavern', 'Inn')
		return random.choice(bldgtypes)

	def get_rooms(self, rooms):
		#trouble here
		d = {
			'Shack':['Entry','Kitchen','Common Area'],
			'Residence':['Entry','Kitchen','Living Area','Dining Area',
				'Common Area', 'Sleeping Quarters'],
			'General Store':['Entry','Store Room', 'Counter'],
			'Armorer':['Entry','Forge', 'Counter'],
			'Livestock Area':['Gate','Barn','Slaughter Room'],
			'Weapon Smith':['Entry','Forge', 'Counter',
				'Grinding Wheel'],
			'Tavern':['Entry','Kitchen','Dining Area', 'Harlot Room'],
			'Inn':['Entry','Kitchen',
				'Common Area', 'Sleeping Quarters']
			}


		roomTypes = d[self.bldgDat['Purpose']]
		
		room_type = random.choice(roomTypes)
		
		roomDat = [{
			'Actors':self.get_inhabitants(random.randint(1,3)),
			'Type':random.choice(roomTypes)
			}for k in xrange(0,rooms)]
		return roomDat

	def get_inhabitants(self, popul):
		inhabitants = {}
		for inhabitant in xrange(0,popul):
			#personType = random.choice(('Commoner', 'Merchant',
			#				'Storekeeper', 'Peasant', 'Noble'))
			person = charGen.main()
			key_name = person['Name']
			inhabitants[key_name] = person
		return inhabitants

def main(opt, biome):
	'''
	Used to interface with townGen.
	'''

	if opt == 'town':
		bldg = Building(biome)
		return bldg.bldgDat
	else:
		bldg = Building('forest')
		neatDicPrint(bldg.bldgDat)
		return 0

if __name__ == '__main__':
	main(None,None)

