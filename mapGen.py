#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  mapGen.py
#  
#  Copyright 2015 Tyler Dinsmoor <d@D-LM>
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

'''
Indended to take data from landGen, bldgGen, townGen, and create pngs
from their data, to be piped to an interface for easier descriptors for
DMs.

Requirements:
	Accept data from:
		landGen:
			biome
			terrain
			fauna
			roads
			water
		bldgGen:
			rooms
			levels
			inhabitants
			purpose
		townGen:
			streets => names
			bldgs/street
'''

class LandImg(object):
	'''
	All data needed to create a new image representing a land-generated
	area.
	'''
	
	def __init__(self):
		pass
		
class BldgImg(object):
	'''
	All data needed to create a new image representing a Bldg-generated
	area.
	'''
	
	def __init__(self):
		pass
		
class TownImg(object):
	'''
	All data needed to create a new image representing a Town-generated
	area.
	'''
	
	def __init__(self):
		pass
		
	


def main():
	
	return 0

if __name__ == '__main__':
	main()

