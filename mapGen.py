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
		cityName,biome,floraDensity,faunaDensity,waterDensity,roadDensity = landGen.main('map')
		self.im = Image.new('RGB',(512,512),'limegreen')
		self.im = self.drawBiome(biome)
		
		self.im = self.drawWater(waterDensity)
		self.im = self.drawTerrain(biome)
		self.im = self.drawFlora(biome)
		self.im = self.drawCity(cityName)
		self.im = self.drawCamps()
		self.im = self.drawVillage()
		
		print biome
		self.showImg()
		
		
	def drawBiome(self,biome):
		draw = ImageDraw.Draw(self.im)
		biomeColors={
		'forest':'limegreen','marsh':'olivedrab',
		'plains':'springgreen','hills':'limegreen',
		'tundra':'lightslategray','desert':'goldenrod'
		}
		draw.rectangle((0,0,self.im.size[0],self.im.size[0]), fill=biomeColors[biome])
		del draw
		return self.im
	
	def drawCity(self,cityName):
		draw = ImageDraw.Draw(self.im)
		x = random.randrange(10,490)
		y = random.randrange(10,490)
		
		draw.polygon(((x,y),(x,y+5),(x+5,y+5),(x+5,y),(x+10,y),
		(x+10,y+5),(x+15,y+5),(x+15,y),(x+20,y),(x+20,y+5),(x+20,y+15),
		(x-5,y+15),(x-5,y)) , fill='grey', outline='lightgrey')
		
		draw.text((x-4,y+12),str(cityName))
		
		del draw
		return self.im
		
	def drawVillage(self):
		draw = ImageDraw.Draw(self.im)
		density = random.randint(1,3)
		for c in xrange(0,density):
			x = random.randrange(10,490)
			y = random.randrange(10,490)
			draw.polygon(((x,y),(x-10,y-10),(x+10,y-10)), fill='olive', outline='orchid')
			draw.rectangle((x+10,y,x-20,y+10), fill='darkolivegreen', outline='lawngreen')
			draw.text((x-4,y+2),"Villiage"+str(c+1))
		
		del draw
		return self.im
		
	def drawCamps(self):
		draw = ImageDraw.Draw(self.im)
		density = random.randint(1,3)
		for c in xrange(0,density):
			x = random.randrange(10,490)
			y = random.randrange(10,490)
			draw.polygon(((x,y),(x+5,y+5),(x-5,y+5)), fill='crimson', outline='red')
			
			draw.text((x-4,y+4),"Camp"+str(c+1))
		
		del draw
		return self.im
		




	def drawTerrain(self,biome):
		
		def hills():
			draw = ImageDraw.Draw(self.im)
			density = random.randint(1,3)
			for c in xrange(0,density*100):
				x = random.randint(0,500)
				y = random.randint(0,500)
				draw.arc((x,y,x+20,y+20),220,340)
			del draw
		
		if biome == 'hills':
			hills()
		
		return self.im
		
		
	def drawWater(self,density):
		draw = ImageDraw.Draw(self.im)
		streamCount = density + (density+2)
		for c in xrange(0,streamCount):
			if random.choice((True,False)) == True:
				x = random.randrange(0,512)
				y = 0
			else:
				x = 0
				y = random.randrange(0,512)
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
				draw.point((x,y), fill='navy')
		del draw
		return self.im

	def drawFlora(self,biome):
		def trees(density):
			density = density*225
			draw = ImageDraw.Draw(self.im)
			#trees
			for c in xrange(0,int(density)+3):
				x = random.randrange(0,512)
				y = random.randrange(0,512)
				draw.ellipse((x, y, x+10, y+10), fill = 'darkgreen', outline ='green')
				#some mild humor
				#draw.text((x-4,y+4),"Tree"+str(c))
			del draw
		
		d ={
		'forest':random.randint(2,4),
		'plains':0.7,
		'hills':0.5,
		'tundra':0.2,
		'marsh':1,
		'desert':0.1
		}
		
		trees(d[biome])
		
		return self.im

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

