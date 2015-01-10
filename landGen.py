#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  areaGen.py
#
#  Copyright 2014 Tyler Dinsmoor <d@D-LM>
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
#  NOTE: Really... REALLY needs to be redone


'''
New requirements for landGen:
Must get:
	Biome
	Techlevel
	Difficulty
	Terrain
	Civilization basics:

'''

import random, argparse
from libdndGen import *

parser = argparse.ArgumentParser(prog='python areaGen.py', description='Creates a description for an area for DnDv5.')
parser.add_argument('-b',metavar='BIOME', help='force biome during creation')
parser.add_argument('-c',metavar='CITY SIZE', help='force a settlement')
args = parser.parse_args()
#will set to None if no argument

biome_override 	= args.b
civ_override	= args.c

if biome_override != None:
	biome_override = biome_override.lower()
if civ_override != None:
	civ_override = civ_override.lower()
'''
 NOTE!!!
 Need to change everything that is a list and the data will not be manipulated
 into a tuple, so long as you are only checking for truth or existance,
 and not for index, or to pop or append anything.
 This can be done with either li = tuple(li) to be easy, or
 they really should be rewritten as (('a'),('b')) instead of [('a'),('b')]
'''
def getBiome():
	#global biome
	biomeList = ('forest','plains','marsh','hills','mountains','desert')
	biomeLeanVal = (('marsh' ,1.0),('plains'  ,5.0),
					('hills' ,1.5),('mountain',1.0),
					('desert',2.0),('forest'  ,3.0))
	biome = wChoice(biomeLeanVal)
	if biome_override in biomeList:
		biome = biome_override
	return biome



def getTerrainForest():
		forestTypeList 			= [('sparse',2.0),('medium',2.0),('dense',1.0)]
		forestTypeFin			= wChoice(forestTypeList)
		forestTreesList 		= [('massive trees',2.0),('typical trees',3.0),('saplings',1.0)]
		forestTreesFin			= wChoice(forestTreesList)
		forestUndergrowthList 	= [('light',2.0),('heavy',3.0)]
		forestUndergrowthFin	= wChoice(forestUndergrowthList)
		return forestTypeFin, forestTreesFin, forestUndergrowthFin

def getTerrainPlains():
		plainsTypeList 			= [('farm',2.0),('grassland',3.0),('battlefield',1.0)]
		plainsTypeFin			= wChoice(plainsTypeList)
		plainsUndergrowthList 	= [('light',4.0),('heavy',1.0)]
		plainsUndergrowthFin	= wChoice(plainsUndergrowthList)
		return plainsTypeFin, plainsUndergrowthFin

def getTerrainMarsh():
		marshTypeList 			= [('moor',3.0),('swamp',2.0)]
		marshTypeFin			= wChoice(marshTypeList)
		marshUndergrowthList 	= [('light',3.0),('heavy',5.0)]
		marshUndergrowthFin		= wChoice(marshUndergrowthList)
		return marshTypeFin, marshUndergrowthFin

def getTerrainHills():
		hillsTypeList 			= [('gentle',3.0),('rugged',2.0)]
		hillsTypeFin			= wChoice(hillsTypeList)
		hillsUndergrowthList 	= [('light',4.0),('heavy',1.0)]
		hillsUndergrowthFin		= wChoice(hillsUndergrowthList)
		return hillsTypeFin, hillsUndergrowthFin

def getTerrainMountain():
		mountainTypeList 			= [('alpine medow',3.0),('rugged',2.0),('forbidding',1.0)]
		mountainTypeFin				= wChoice(mountainTypeList)
		mountainUndergrowthList 	= [('light',4.0),('heavy',1.0)]
		mountainUndergrowthFin		= wChoice(mountainUndergrowthList)
		return mountainTypeFin, mountainUndergrowthFin

def getTerrainDesert():
		desertTypeList 				= [('tundra',0.5),('rocky',3.0),('sandy',2.0)]
		desertTypeFin				= wChoice(desertTypeList)
		desertUndergrowthList 		= [('light',2.0),('no',1.0)]
		desertUndergrowthFin		= wChoice(desertUndergrowthList)
		return desertTypeFin, desertUndergrowthFin

# data is important, will need to influence techlevel,
# as it's hard to get teachnology if you don't have much
# food resources
def getFauna():
	print

def getRoads():
	pass

# see comment on getFauna
def getWater():
	pass


# needs to be readone, and settlement names be added to
# an external file for easy editing (see charGen; getSpells)
# but a slightly different approach may be needed due to the
# probability problem... but in reality it would be best to just
# add logic for whether or not there will be a civilization, due to
# what's written below not making any logical sense in the long run.
#
# but, for activity sake, it would be better for there to be ALWAYS
# a city, but have it to where how advanced it was mattered much more than
# anything else in logic. Most of this file needs to be redone.
def getCiv():
	global techLevel
	techLevelPoss 			= (('primitive', 2.0),('average',5.0),('advanced',0.5))
	mainDispositionPoss		= (('hostile',1.0),('neutral',3.0),('friendly',0.5))
	outerDispositionPoss	= (('hostile',2.0),('neutral',3.0),('friendly',2.0))
	largeSettlementNames	= (('Antioka'),	('Falenshire'),	('Reust'),
							('Perdale'),	('Avergio'),	('Kurbright'),	('Protrm'),
							('Locksteen'),	('Denpolor'),	('Lorkin'),		('Remalved'),
							('Antrag'),		('Ystar'),		('Enquindor'),	('Kilmen'),
							('Lofory'),		('Stillmarch'),	('Slumberwood'),('Silverwatch'),
							('Bruma'),		('Chapsworth'),	('Dharenvale'),	('Parthel'),
							('Florin'),		('Chiddy'),		('Kalath'),		('Redwood Reach'))
	allSettlementNames 		= getFromFile_T('data/cities')
	techLevel 		= wChoice(techLevelPoss)
	civMainDisposition 	= wChoice(mainDispositionPoss)
	civOuterDisposition	= wChoice(outerDispositionPoss)
	civSettlement 		= random.choice(allSettlementNames)
	if civSettlement in largeSettlementNames:
		civIsLargeSettlement = True
	else:
		civIsLargeSettlement = False
	while (civ_override == 'large') and (civIsLargeSettlement == False):
		civSettlement = wChoice(allSettlementNames)
		if civSettlement in largeSettlementNames:
			civIsLargeSettlement = True
		else:
			civIsLargeSettlement = False
	while (civ_override == 'small') and ((civIsLargeSettlement == True) or (civSettlement == 'NONE')):
		civSettlement = wChoice(allSettlementNames)
		if civSettlement in largeSettlementNames:
			civIsLargeSettlement = True
		else:
			civIsLargeSettlement = False

	return techLevel, civMainDisposition, civOuterDisposition, civSettlement, civIsLargeSettlement
#
#most data proc should be above here
#
def main(infoReq):
	biome = getBiome()
	techLevel, civMainDisposition, civOuterDisposition, civSettlement, civIsLargeSettlement = getCiv()
	if biome == 'forest':
		typeFin, treesFin, undergrowthFin = getTerrainForest()
	elif biome == 'plains':
		typeFin, undergrowthFin = getTerrainPlains()
	elif biome == 'marsh':
		typeFin, undergrowthFin = getTerrainMarsh()
	elif biome == 'hills':
		typeFin, undergrowthFin = getTerrainHills()
	elif biome == 'mountain':
		typeFin, undergrowthFin = getTerrainMountain()
	elif biome == 'desert':
		typeFin, undergrowthFin = getTerrainDesert()
	if infoReq == "bldg":
		return biome, techLevel
	else:
		print "Wrong Designator"
	print civSettlement
