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
def getBiome():
	#global biome
	biomeList = ('forest','plains','marsh','hills','tundra','desert')
	biomeLeanVal = (('marsh' ,1.0),('plains'  ,5.0),
					('hills' ,1.5),('tundra',1.0),
					('desert',2.0),('forest'  ,3.0))
	biome = wChoice(biomeLeanVal)
	if biome_override in biomeList:
		biome = biome_override
	return biome


def getCiv():
	cityname = random.choice(getFromFile_T('data/cities'))
	for s in cityname:
		return s

#
#most data proc should be above here
#
def main(infoReq):
	
	biome = getBiome()
		
	# 0 is pre-stone age, 3 is dark age
	techLevel 		= random.randint(0,3)
	# 0 is sparse, 5 is very dense
	floraDensity	= random.randint(0,5)
	faunaDensity	= random.randint(0,5)
	waterDensity	= random.randint(0,5)
	roadDensity		= random.randint(0,5)
	
	
	if infoReq == "bldg":
		return biome, techLevel
	elif infoReq == 'map':
		return getCiv(),biome,floraDensity,faunaDensity,waterDensity,roadDensity
	else:
		print "Wrong Designator"
	print civSettlement
