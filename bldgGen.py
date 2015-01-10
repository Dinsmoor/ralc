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
	def __init__(self, bldgID):
		self.bldgID = bldgID

	def getPurpose(self):
		pass

	def getInhabitants(self, popul):
		peopleDat = {}
		for inhabitant in xrange(0,popul):

			personType = random.choice(('Commoner', 'Peasant', 'Noble'))
			peopleDat[personType+str(inhabitant)] = charGen.main()
			#neatDicPrint(peopleDat[peopleID])
		return peopleDat

	def getRooms(self):
		'''
		Should represent rooms as multiple dicts, but with spontaniously created vars
		Need: Size, Furnishings, inhabitants
		'''
		roomDat = {}
		roomDat['rooms'] = 3
		count = 0
		for roomnum in xrange(0,roomDat['rooms']):
			popul = random.randint(1,3)
			roomNames = ('Entry','Kitchen','Living Area')
			roomDat['roomID'+str(count)] = random.choice(roomNames)+str(roomnum)
			#roomDat['roomID'] = Room(roomID, rooms, popul)
			roomDat['Inhabitants'] = self.getInhabitants(popul)
			count +=1

		return roomDat

	def getType(self):
		bldgtypes = ('Shack','Residence','General Store','Armorer','Courtyard',
	'Weapon Smith', 'Tavern', 'Inn')
		return random.choice(bldgtypes)
	def getLevels(self):
		return random.randint(1,2)
	def getBldgMake(self):
		descDict = {
		#techlevel:roofing,walls,floor
		'primitive':(('thatch','straw'),('stick','mud'),('dirt','straw')),
		'average':(('wooden','shingle'),('boarded','log','stone'),('wooden','stone')),
		'advanced':(('sheet metal','shingle'),('concrete','stone','metal'),('wooden','metal','tile'))
		}
		materialsTup = descDict[techLevel]

		return (random.choice(materialsTup[0]),random.choice(materialsTup[1]),random.choice(materialsTup[2]))


	def getAll(self):
		self.btype = self.getType()
		self.levels = self.getLevels()
		self.make = self.getBldgMake()
		self.roomDat = self.getRooms()
		'''
		rooms is important, it determines the types of rooms, how many
		inhabitants, and then gets their data from chargen.
		'''
	def giveDesc(self):
		print '''
Techlevel is %s.
		''' % techLevel
		print '''
The %s has %s rooms and %d floors.
The roof is made of %s, walls %s, and floor %s.''' % (self.btype,self.roomDat['rooms'],self.levels,self.make[0],self.make[1],self.make[2])
		#print self.roomDat
		neatDicPrint(self.roomDat)
		#print self.bldgID

def makeBuilding(num):
	c = 0
	for x in xrange(0,num):
		a = Building(c)
		a.getAll()
		a.giveDesc()
		c +=1


def getConstruction(biome, techLevel):
	print biome, techLevel
	materialList = ['logs','thatch','underground','stone']
	if biome == "forest":
		material = materialList[0]
	elif biome == "plains":
		material = materialList[1]
	elif biome == "marsh":
		material = materialList[1]
	elif biome == "hills":
		material = random.choice(materialList)
	elif biome == "mountain":
		material = materialList[3]
	elif biome == "desert":
		material = materialList[2]

	if material == materialList[0]:
		constDesc = ""
	elif material == materialList[1]:
		constDesc = ""
	elif material == materialList[2]:
		constDesc = ""
	elif material == materialList[3]:
		constDesc = ""
	bldgDesc='''
	The buildings in this area are of %s constructon,
	due to the %s-like area.
	'''%(material,biome)


def getBldgType():
	typeList= ['Shack','Residence','General Store','Armorer','Courtyard',
	'Weapon Smith', 'Tavern', 'Inn']
	# ie. store, armorer, residence, public area
	# mostly random
def getNumOfResidents():
	# dependant on building type and
	pass

#getConstruction(biome, TechLevel)

def main():
	makeBuilding(1)
	return 0

if __name__ == '__main__':
	main()

