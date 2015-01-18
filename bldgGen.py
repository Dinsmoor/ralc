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

import landGen
from libdndGen import *
import charGen
biome, techLevel = landGen.main("bldg")

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

class Building(object):
	'''
	Building needs walls, height, max inhabitatants, purpose
	'''
	def __init__(self, bldgID,levels,rooms):
		self.bldgID = bldgID
		self.btype = self.getPurpose()
		self.levels = levels #self.getLevels()
		self.make = self.getBldgMake()
		self.roomDat = self.getRooms(rooms)

	def getInhabitants(self, popul):
		peopleDat = {}
		for inhabitant in xrange(0,popul):

			personType = random.choice(('Commoner', 'Merchant', 'Storekeeper', 'Peasant', 'Noble'))
			peopleDat[personType+str(inhabitant)] = charGen.main()
			#neatDicPrint(peopleDat[peopleID])
		return peopleDat

	def getRooms(self, rooms):
		'''
		Should represent rooms as multiple dicts, but with spontaniously created vars
		Need: Size, Furnishings, inhabitants
		'''
		roomDat = {}
		roomDat['rooms'] = rooms
		count = 0
		for roomnum in xrange(0,roomDat['rooms']):
			popul = random.randint(1,3)
			roomNames = ('Entry','Kitchen','Living Area')
			roomDat['roomID'+str(count)] = random.choice(roomNames)+str(roomnum)
			#roomDat['roomID'] = Room(roomID, rooms, popul)
			roomDat['roomID'+str(count)+'Inhabitants'] = self.getInhabitants(popul)
			count +=1

		return roomDat

	def getPurpose(self):
		'''
		In the future, will be determined by what civGen needs, but used
		here for debugging purposes. Same with getLevels.
		'''
		bldgtypes = ('Shack','Residence','General Store','Armorer','Courtyard',
	'Weapon Smith', 'Tavern', 'Inn')
		return random.choice(bldgtypes)


	def getBldgMake(self):
		descDict = {
		#techlevel:roofing[0],walls[1],floor[2]
		1:(('thatch','straw'),('stick','mud'),('dirt','straw')),
		2:(('wooden','shingle'),('boarded','log','stone'),('wooden','stone')),
		3:(('sheet metal','shingle'),('concrete','stone','metal'),('wooden','metal','tile'))
		}
		materialsTup = descDict[techLevel]

		return (random.choice(materialsTup[0]),random.choice(materialsTup[1]),random.choice(materialsTup[2]))

	def giveDesc(self):
		'''
		Currently a debugging/dumping area to dump data prior to actual
		use in ralc main.
		'''
		print '''
Techlevel is %d.
		''' % techLevel
		print '''
The %s has %s rooms and %d floors.

The roof is made of %s, walls %s, and floor %s.''' % (self.btype,
		self.roomDat['rooms'],self.levels,

		self.make[0],self.make[1],self.make[2])
		#print self.roomDat
		neatDicPrint(self.roomDat)
		#print self.bldgID

def makeBuilding(num,levels,rooms):
	'''
	# of bldgs, size
	Handles the rules from civGen that each building needs to obey and
	conform to. This will be size, levels, stored as a string to have
	values determined for here.
	'''
	c = 0
	for x in xrange(0,num):
		a = Building(c,levels,rooms)
		#a.getAll(levels,rooms)
		a.giveDesc()
		c +=1



def main():
	'''
	This function is only kept until this program is capable of running
	indepentantly and will be removed after the program being debugged.
	'''
	makeBuilding(1,1,2)
	#1 building to make, each with 1 floor, each floor with 1 room
	return 0

if __name__ == '__main__':
	main()

