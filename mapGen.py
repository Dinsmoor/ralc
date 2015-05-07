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
	import random, townGen
	from PIL import Image, ImageDraw, ImageTk
	from libdndGen import *
except ImportError:
	print "You are missing essential Libraries. See README.md"


class Land_Image(object):
	'''
	All data needed to create a new image representing a land-generated
	area.
	'''

	def __init__(self):
		'''
		Collects needed data to draw on top of a canvas. Order matters!
		'''
		biome = self.get_biome()
		self.biome = biome
		self.camp_name = getCityName()

		# names to be passed to main, filled when drawn
		self.village_names = []
		self.camp_names = []

		# set base img size
		self.imgx = 600
		self.imgy = self.imgx
		# initilize the image
		self.im = Image.new('RGBA',(self.imgx,self.imgy),'limegreen')
		self.draw = ImageDraw.Draw(self.im)

		# start drawing on top of the image
		self.draw_biome(biome)
		self.draw_water(biome)
		self.draw_terrain(biome)
		self.draw_flora(biome)
		self.draw_city()
		self.draw_camps()
		self.draw_village()

		#self.drawKey()
		#self.save_image()
		#self.show_image()
	def get_biome(self):
		biomeLeanVal = (('marsh' ,1.0),('plains'  ,5.0),
						('hills' ,1.5),('tundra',1.0),
						('desert',2.0),('forest'  ,3.0))
		return wChoice(biomeLeanVal)

	def draw_biome(self,biome):

		'''
		# new method for drawing biome, but my images are ugly D;
		image_to_paste = Image.open('data/sprites/'+biome.lower()+str(random.randint(1,3))+'.png')
		self.im.paste(image_to_paste, (0,0), image_to_paste)

		'''
		# These colors are very up for debate. Default HTML colors are ugly
		biomeColors={
		'forest':'#088A08','marsh':'#4B8A08',
		'plains':'#D0FA58','hills':'#D8F781',
		'tundra':'#D8D8D8','desert':'#F7D358'
		}
		self.draw.rectangle((0,0,self.im.size[0],self.im.size[0]),
			fill=biomeColors[biome])

	def draw_city(self):

		x = random.randrange(10,self.imgx-50)
		y = random.randrange(10,self.imgy-50)
		image_to_paste = Image.open('data/sprites/city.png')
		self.im.paste(image_to_paste, (x,y), image_to_paste)
		self.draw.text((x-10,y+18),str(self.camp_name))
		self.city_location = (x,y)

	def draw_village(self):

		density = random.randint(1,3)
		for c in xrange(0,density):
			villageName = getVillageName()
			self.village_names.append(villageName)

			x = random.randrange(10,self.imgx-50)
			y = random.randrange(10,self.imgy-50)
			image_to_paste = Image.open('data/sprites/village.png')
			self.im.paste(image_to_paste, (x,y), image_to_paste)

			self.draw.text((x-10,y+18),'%s'%villageName)
			roadLength = int(gridDistance((self.city_location,(x,y))) / 15) # to be used for km
			self.draw.text((x-10,y+25),'to city: %dkm'%(roadLength))

	def draw_camps(self):

		density = random.randint(1,3)
		for c in xrange(0,density):
			campName = getCampName()
			self.camp_names.append(campName)
			x = random.randrange(10,self.imgx-50)
			y = random.randrange(10,self.imgy-50)
			image_to_paste = Image.open('data/sprites/camp.png')
			self.im.paste(image_to_paste, (x,y), image_to_paste)
			self.draw.text((x-10,y+18),"Camp %s"%campName)
			roadLength = int(gridDistance((self.city_location,(x,y))) / 15) # to be used for km
			self.draw.text((x-10,y+25),'to city: %dkm'%(roadLength))

	def draw_terrain(self,biome):

		def hills():
			density = random.randint(1,3)
			for c in xrange(0,density*100):
				x = random.randint(0,self.imgx)
				y = random.randint(0,self.imgy)
				self.draw.arc((x,y,x+20,y+20),220,340, fill='gray')

		if biome == 'hills':
			pass
			#hills()

	def draw_water(self, biome):

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

	def draw_flora(self,biome):

		def trees(density,artList):

			density = density*225
			#using tree sprites
			for t in xrange(0,int(density)):
				image_to_paste = Image.open('data/sprites/'+random.choice(artList)+'.png')
				x = random.randrange(0,self.imgx)
				y = random.randrange(0,self.imgy)
				self.im.paste(image_to_paste, (x,y), image_to_paste)

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

	def draw_road(self,targetCoord):

		# draws line from each villiage to city
		# self.draw.line((self.city_location,self.villageCoord), fill='gray')
		roadLength = gridDistance((self.city_location,targetCoord))
		return roadLength

	def save_image(self):
		self.im.save('landMap', "PNG")

	def show_image(self):
		self.im.show()


class Town_Image(Land_Image):
	'''
	All data needed to create a new image representing a Town-generated
	area.
	'''

	def __init__(self):
		#get cityname from Land_Image
		self.camp_name = landImg.camp_name
		self.streets = townGen.main('map',1,landImg.biome)


		self.imgx = 600
		self.imgy = self.imgx
		# initilize the image
		self.im = Image.new('RGB',(self.imgx,self.imgy),'lightgray')
		self.draw = ImageDraw.Draw(self.im)

		self.drawStreets()
		self.drawWalls()

	def drawBldgs(self):
		pass

	def drawWalls(self):

		img_city_walls = Image.open('data/sprites/cityWalls.png')
		self.im.paste(img_city_walls, (0,0), img_city_walls)

	def drawStreets(self):
		img_bldgSimple = Image.open('data/sprites/cityBldgSimple.png')
		total_streets = len(self.streets)
		street_interval = self.imgx / total_streets

		x_axis_assigned = random.randint(1, total_streets -1)
		y_axis_assigned = total_streets - x_axis_assigned
		bldg_interval = 6

		# for debugging
		#print 'Streets:'
		#print self.streets
		#for street, bldgs in self.streets.iteritems():
		#	print street
		#	print bldgs[0]['Rooms'][0][0]['Actors'][0]['Name']

		#print "Total Streets: %d"%len(self.streets)
		#print "Street Interval: %d" %street_interval

		x = 0 - (street_interval / 2)
		y = x

		x_interval = self.imgx / x_axis_assigned
		y_interval = self.imgy / y_axis_assigned

		for street in xrange(x_axis_assigned):
			x += x_interval
			self.draw.line((x,20,x,580), fill='#9A8857', width=3)
			for bldg in xrange(1,6):
				bldg_y = self.imgy / bldg
				self.im.paste(img_bldgSimple, (x-10,bldg_y), img_bldgSimple)

		for street in xrange(y_axis_assigned):
			y += y_interval
			self.draw.line((20,y,580,y), fill='#9A8857', width=3)
			for bldg in xrange(1,6):
				bldg_x = self.imgx / bldg
				self.im.paste(img_bldgSimple, (bldg_x,y-10), img_bldgSimple)

	def drawLots(self):
		pass

	def save_image(self):
		self.im.save('landMap', "PNG")

	def show_image(self):
		self.im.show()

class Building_Image(Town_Image):
	'''
	All data needed to create a new image representing a Bldg-generated
	area.
	'''

	def __init__(self):
		#get cityname from Land_Image
		self.camp_name = landImg.camp_name
		self.imgx = 600
		self.imgy = self.imgx
		# initilize the image
		self.im = Image.new('RGB',(self.imgx,self.imgy),'maroon')
		self.draw = ImageDraw.Draw(self.im)


	def save_image(self):
		self.im.save('landMap', "PNG")

	def show_image(self):
		self.im.show()

def main(opt):
	global landImg, townImg, bldgImg
	if opt == 'tk':
		landImg = Land_Image()
		townImg = Town_Image()
		bldgImg = Building_Image()
		return (landImg.im, landImg.camp_name,
			landImg.village_names ,landImg.camp_names,
			townImg.streets)
	else:
		landImg = Land_Image()
		townImg = Town_Image()
		bldgImg = Building_Image()
		townImg.show_image()

		return 0

if __name__ == '__main__':
	main('')

