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
Need: python-imaging, python-imaging-tk, pyhton-matplotlib, python-numpy

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

import Image, ImageDraw, ImageTk, sys, landGen, random
from libdndGen import *

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
		biome = self.getBiome()
		self.cityName = getCityName()

		self.imgx = 600
		self.imgy = self.imgx

		self.im = Image.new('RGB',(self.imgx,self.imgy),'limegreen')
		self.draw = ImageDraw.Draw(self.im)


		self.drawBiome(biome)
		self.drawWater()
		self.drawTerrain(biome)
		self.drawFlora(biome)
		self.drawCity(self.cityName)
		self.drawCamps()
		self.drawVillage()
		#self.drawKey()

		#self.saveImg()
		#self.showImg()
	def getBiome(self):
		biomeLeanVal = (('marsh' ,1.0),('plains'  ,5.0),
						('hills' ,1.5),('tundra',1.0),
						('desert',2.0),('forest'  ,3.0))
		return wChoice(biomeLeanVal)

	def drawBiome(self,biome):
		biomeColors={
		'forest':'limegreen','marsh':'olivedrab',
		'plains':'springgreen','hills':'limegreen',
		'tundra':'lightslategray','desert':'goldenrod'
		}
		self.draw.rectangle((0,0,self.im.size[0],self.im.size[0]), fill=biomeColors[biome])


	def drawCity(self,cityName):
		x = random.randrange(10,490)
		y = random.randrange(10,490)
		self.cityShape = ((x,y),(x,y+5),(x+5,y+5),(x+5,y),(x+10,y),
		(x+10,y+5),(x+15,y+5),(x+15,y),(x+20,y),(x+20,y+5),(x+20,y+15),
		(x-5,y+15),(x-5,y))
		self.draw.polygon(self.cityShape, fill='grey', outline='lightgrey')
		self.draw.text((x-4,y+12),str(cityName))
		self.cityCoord = (x,y)


	def drawVillage(self):
		density = random.randint(1,3)
		for c in xrange(0,density):
			x = random.randrange(10,490)
			y = random.randrange(10,490)
			self.villageShape = ((x,y),(x-10,y-10),(x+10,y-10))
			self.villageCoord = (x,y)
			roadLength = self.drawRoad() / 10 # to be used for km
			self.draw.polygon(self.villageShape, fill='olive',
				outline='orchid')
			self.draw.rectangle((x+10,y,x-20,y+10), fill='darkolivegreen',
				outline='lawngreen')
			self.draw.text((x-4,y+2),'%s'%getVillageName())
			self.draw.text((x-4,y+8),'to %s: %dkm'%(self.cityName, roadLength))



	def drawCamps(self):

		density = random.randint(1,3)
		for c in xrange(0,density):
			x = random.randrange(10,490)
			y = random.randrange(10,490)
			self.campShape = (x,y),(x+5,y+5),(x-5,y+5)
			self.draw.polygon((self.campShape),
				fill='crimson', outline='red')
			self.draw.text((x-4,y+4),"Camp %s"%getCampName())


	def drawTerrain(self,biome):
		def hills():

			density = random.randint(1,3)
			for c in xrange(0,density*100):
				x = random.randint(0,500)
				y = random.randint(0,500)
				self.draw.arc((x,y,x+20,y+20),220,340)

		if biome == 'hills':
			hills()



	def drawWater(self):
		density = random.randint(0,5)
		streamCount = density + (density+2)
		for c in xrange(0,streamCount):
			if random.choice((True,False)) == True:
				x = random.randrange(0,self.imgx)
				y = 0
			else:
				x = 0
				y = random.randrange(0,self.imgy)
			for null in xrange(0,8000):
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
				self.draw.point((x,y), fill='navy')


	def drawFlora(self,biome):
		def trees(density):
			density = density*225

			#trees
			for c in xrange(0,int(density)):
				x = random.randrange(0,self.imgx)
				y = random.randrange(0,self.imgy)
				self.draw.ellipse((x, y, x+10, y+10), fill = 'darkgreen',
					outline ='green')
				#some mild humor
				#draw.text((x-4,y+4),"Tree"+str(c))


		# Tree ensity Modifiers
		d ={
		'forest':random.randint(2,4),
		'plains':0.7,
		'hills':0.5,
		'tundra':0.2,
		'marsh':1,
		'desert':0.1
		}

		trees(d[biome])

	def drawRoad(self):
		# draws line from each villiage to city
		# self.draw.line((self.cityCoord,self.villageCoord), fill='gray')
		roadLength = gridDistance((self.cityCoord,self.villageCoord))
		return roadLength

	def drawKey(self):
		self.draw.rectangle((5,5,10,10), fill='black')
		#self.draw.polygon(, fill='white')

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



#landImg = LandImg()

def main(opt):
	if opt == 'tk':
		landImg = LandImg()
		return landImg.im, landImg.cityName
	else:
		landImg = LandImg()
		return 0

if __name__ == '__main__':
	main('')

