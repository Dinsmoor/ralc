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

import Image, ImageDraw, sys, landGen, random

class LandImg(object):
	'''
	All data needed to create a new image representing a land-generated
	area.
	'''

	def __init__(self):
		'''
		Need:
			biome
			terrain
			fauna
			flora
			roads
			water
		'''
		floraDensity,faunaDensity,waterDensity,roadDensity = landGen.main('map')
		self.im = Image.new('RGB',(512,512),'white')
		self.im = self.drawBiome()
		self.im = self.drawTerrain()
		#self.im = self.drawWater(waterDensity)
		self.showImg()


	def drawBiome(self):
		draw = ImageDraw.Draw(self.im)
		draw.rectangle((0,0,self.im.size[0],self.im.size[0]), fill='brown')
		#draw.line((0, 0) + self.im.size, fill=128)
		#draw.line((200, 0) + self.im.size, fill=128)

		#draw.line((0, self.im.size[1], self.im.size[0], 0), fill=128)
		self.draw = draw
		return self.im



	def drawTerrain(self):
		terrain = 'forrest'
		density = 3
		draw = ImageDraw.Draw(self.im)
		draw.circle(50)

		for c in xrange(5,(density+3)):
			draw.ellipse((100,100,200,100), fill='green')

		return self.im
	def drawWater(self,density):
		draw = ImageDraw.Draw(self.im)
		streamCount = density + (density+2)
		for c in xrange(0,streamCount):
			#if random.choice((True,False)) == True:
			x = random.randrange(0,512)
			y = random.randrange(0,512)
			for null in xrange(0,10000):
				if random.choice((True,False)) == True:
					if random.randint(0,9) > random.randint(0,9):
						x -= 1
					else:
						x += 1
				else:
					if random.randint(0,9) > random.randint(0,9):
						y -= 1
					else:
						y += 1
				draw.point((x,y), fill='blue')

		return self.im

	def drawFlora(self):
		pass

	def saveImg(self):
		self.im.save('landMap', "PNG")

	def showImg(self):
		self.im.show()

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



landImg = LandImg()

def main():

	return 0

if __name__ == '__main__':
	main()

