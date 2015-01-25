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
Need: python-pil, python-pil.imagetk, pyhton-matplotlib, python-numpy

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
try:
	import random
	from PIL import Image, ImageDraw, ImageTk
	from libdndGen import *
except ImportError:
	print "You are missing essential Libraries. See README.md"

def make_bezier(xys):
	# xys should be a sequence of 2-tuples (Bezier control points)
	n = len(xys)
	combinations = pascal_row(n-1)
	def bezier(ts):
		# This uses the generalized formula for bezier curves
		# http://en.wikipedia.org/wiki/B%C3%A9zier_curve#Generalization
		result = []
		for t in ts:
			tpowers = (t**i for i in range(n))
			upowers = reversed([(1-t)**i for i in range(n)])
			coefs = [c*a*b for c, a, b in zip(combinations, tpowers, upowers)]
			result.append(
				tuple(sum([coef*p for coef, p in zip(coefs, ps)]) for ps in zip(*xys)))
		return result
	return bezier

def pascal_row(n):
	# This returns the nth row of Pascal's Triangle
	result = [1]
	x, numerator = 1, n
	for denominator in range(1, n//2+1):
		# print(numerator,denominator,x)
		x *= numerator
		x /= denominator
		result.append(x)
		numerator -= 1
	if n&1 == 0:
		# n is even
		result.extend(reversed(result[:-1]))
	else:
		result.extend(reversed(result))
	return result


class LandImg(object):
	'''
	All data needed to create a new image representing a land-generated
	area.
	'''

	def __init__(self):
		'''
		Collects needed data to draw on top of a canvas. Order matters!
		'''
		biome = self.getBiome()
		self.cityName = getCityName()

		# names to be passed to main, filled when drawn
		self.villageNames = []
		self.campNames = []

		# set base img size
		self.imgx = 600
		self.imgy = self.imgx
		# initilize the image
		self.im = Image.new('RGBA',(self.imgx,self.imgy),'limegreen')
		self.draw = ImageDraw.Draw(self.im)

		# start drawing on top of the image
		self.drawBiome(biome)
		self.drawWater(biome)
		self.drawTerrain(biome)
		self.drawFlora(biome)
		self.drawCity()
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
		pasteIm = Image.open('data/sprites/'+biome.lower()+str(random.randint(1,3))+'.png')
		self.im.paste(pasteIm, (0,0), pasteIm)

		'''
		# old method for bullshit
		# These colors are very up for debate. Default HTML colors are ugly
		biomeColors={
		'forest':'olivedrab','marsh':'olivedrab',
		'plains':'olivedrab','hills':'olivedrab',
		'tundra':'lightslategray','desert':'goldenrod'
		}
		self.draw.rectangle((0,0,self.im.size[0],self.im.size[0]),
			fill=biomeColors[biome])
		'''

	def drawCity(self):
		x = random.randrange(10,self.imgx-50)
		y = random.randrange(10,self.imgy-50)
		pasteIm = Image.open('data/sprites/city.png')
		self.im.paste(pasteIm, (x,y), pasteIm)
		self.draw.text((x-10,y+18),str(self.cityName))
		self.cityCoord = (x,y)

	def drawVillage(self):
		density = random.randint(1,3)
		for c in xrange(0,density):
			villageName = getVillageName()
			self.villageNames.append(villageName)

			x = random.randrange(10,self.imgx-50)
			y = random.randrange(10,self.imgy-50)
			pasteIm = Image.open('data/sprites/village.png')
			self.im.paste(pasteIm, (x,y), pasteIm)

			self.draw.text((x-10,y+18),'%s'%villageName)
			roadLength = int(gridDistance((self.cityCoord,(x,y))) / 15) # to be used for km
			self.draw.text((x-10,y+25),'to city: %dkm'%(roadLength))

	def drawCamps(self):
		density = random.randint(1,3)
		for c in xrange(0,density):
			campName = getCampName()
			self.campNames.append(campName)
			x = random.randrange(10,self.imgx-50)
			y = random.randrange(10,self.imgy-50)
			pasteIm = Image.open('data/sprites/camp.png')
			self.im.paste(pasteIm, (x,y), pasteIm)
			self.draw.text((x-10,y+18),"Camp %s"%campName)
			roadLength = int(gridDistance((self.cityCoord,(x,y))) / 15) # to be used for km
			self.draw.text((x-10,y+25),'to city: %dkm'%(roadLength))

	def drawTerrain(self,biome):
		def hills():
			density = random.randint(1,3)
			for c in xrange(0,density*100):
				x = random.randint(0,self.imgx)
				y = random.randint(0,self.imgy)
				self.draw.arc((x,y,x+20,y+20),220,340, fill='gray')

		if biome == 'hills':
			pass
			#hills()

	def drawWater(self, biome):
		def river(densityFactor):
			density = random.randint(0,5)
			streamCount = int(density + (density*densityFactor))
			for c in xrange(0,streamCount):
				# determines whether to start on x or y axis
				if random.choice((True,False)):
					x = random.randrange(0,self.imgx)
					y = 0
				else:
					x = 0
					y = random.randrange(0,self.imgy)
				for null in xrange(0,10000):
					# decides which direction to wander
					if random.choice((True,False)):
						if random.randint(0,9) > random.randint(0,9):
							x -= 1
						else:
							x += 1
						if (x >= self.imgx):
							break
					else:
						if random.randint(0,9) > random.randint(0,9):
							y -= 1
						else:
							y += 1
						if (y >= self.imgy):
							break
					self.draw.point((x,y), fill='navy')

		def lake():
			# just have it be a shallow-looking pond, I suppose
			self.draw.ellipse()

		d ={
		'forest':0.7,
		'plains':0.6,
		'hills':0.7,
		'tundra':0.3,
		'marsh':1,
		'desert':0.1
		}
		river(d[biome])

	def drawFlora(self,biome):
		def trees(density,artList):
			density = density*225
			#using tree sprites
			for t in xrange(0,int(density)):
				pasteIm = Image.open('data/sprites/'+random.choice(artList)+'.png')
				x = random.randrange(0,self.imgx)
				y = random.randrange(0,self.imgy)
				self.im.paste(pasteIm, (x,y), pasteIm)

			#old-style trees
			'''
			for c in xrange(0,int(density)):
				x = random.randrange(0,self.imgx)
				y = random.randrange(0,self.imgy)
				self.draw.ellipse((x, y, x+8, y+8), fill = 'darkgreen',
					outline ='green')
				#some mild humor
				#draw.text((x-4,y+4),"Tree"+str(c))
			'''

		# Tree ensity Modifiers
		d ={
		'forest':[random.randint(2,4),('tree1','tree2')],
		'plains':[0.7,	('tree3','desertF1')],
		'hills':[0.5,	('tree3','desertF1')],
		'tundra':[0.2,	('tree3','desertF1')],
		'marsh':[1,		('marshF1','tree2')],
		'desert':[0.1,	('desertF1','desertF2')]
		}

		trees(d[biome][0],d[biome][1])

	def drawRoad(self,targetCoord):
		# draws line from each villiage to city
		# self.draw.line((self.cityCoord,self.villageCoord), fill='gray')
		roadLength = gridDistance((self.cityCoord,targetCoord))
		return roadLength

	def drawKey(self):
		# draw extra icon with label underneath
		self.draw.rectangle((5,5,10,10), fill='black')
		#self.draw.polygon(, fill='white')

	def saveImg(self):
		self.im.save('landMap', "PNG")

	def showImg(self):
		self.im.show()


class TownImg(LandImg):
	'''
	All data needed to create a new image representing a Town-generated
	area.
	'''

	def __init__(self):
		#get cityname from LandImg
		self.cityName = landImg.cityName
		self.imgx = 600
		self.imgy = self.imgx
		# initilize the image
		self.im = Image.new('RGB',(self.imgx,self.imgy),'lightgray')
		self.draw = ImageDraw.Draw(self.im)

	def drawWalls(self):
		pass

	def drawGates(self):
		pass

	def drawStreets(self):
		pass

	def drawLots(self):
		pass

	def saveImg(self):
		self.im.save('landMap', "PNG")

	def showImg(self):
		self.im.show()

class BldgImg(TownImg):
	'''
	All data needed to create a new image representing a Bldg-generated
	area.
	'''

	def __init__(self):
		#get cityname from LandImg
		self.cityName = landImg.cityName
		self.imgx = 600
		self.imgy = self.imgx
		# initilize the image
		self.im = Image.new('RGB',(self.imgx,self.imgy),'maroon')
		self.draw = ImageDraw.Draw(self.im)


	def saveImg(self):
		self.im.save('landMap', "PNG")

	def showImg(self):
		self.im.show()

def main(opt):
	global landImg, townImg, bldgImg
	if opt == 'tk':
		landImg = LandImg()
		townImg = TownImg()
		bldgImg = BldgImg()
		return (landImg.im, landImg.cityName,
			landImg.villageNames ,landImg.campNames)
	else:
		landImg = LandImg()
		townImg = TownImg()
		bldgImg = BldgImg()
		#landImg.showImg()

		return 0

if __name__ == '__main__':
	main('')

