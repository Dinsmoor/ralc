#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  mapGen.py
#
#  Copyright 2015 Tyler Dinsmoor <pappad@airmail.cc>
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

try:
	import random, townGen
	from PIL import Image, ImageDraw, ImageTk
except ImportError:
	print "You are missing essential Libraries. See README.md"
	exit()

def getFromFile_T(fi):
	fi = open(fi)
	li = [i.strip().split('\n') for i in fi if not i.startswith("#")]
	li = [x for x in li if x != ['']]
	tu = tuple(li)
	fi.close()
	return tu

def getSmallName(small_type):
	name = random.choice(getFromFile_T('data/'+small_type.lower()+'s'))
	for s in name:
		return s
def getCityName():
	cityname = random.choice(getFromFile_T('data/cities'))
	for s in cityname:
		return s
def getVillageName():
	villageName = random.choice(getFromFile_T('data/villages'))
	for s in villageName:
		return s
def getCampName():
	campName = random.choice(getFromFile_T('data/camps'))
	for s in campName:
		return s
def getBldgName():
	bldgName = random.choice(getFromFile_T('data/bldgs'))
	for s in bldgName:
		return s
def wChoice(wCh):
	'''must be in format: wChoice(('a',1.0),('b',2.0),('c',3.0))'''
	totalChoice = sum(w for c, w in wCh)
	random_uniform = random.uniform(0, totalChoice)
	upto = 0
	for c, w in wCh:
		if upto + w > random_uniform:
			return c
		upto += w
	assert False, "Shouldn't get here"
def gridDistance(points):
	import math
	p0, p1 = points
	return int(math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2))

class Land_Image(object):
	'''
	All data needed to create a new image representing a land-generated
	area.
	'''

	def __init__(self, biome_ovr):
		'''
		Collects needed data to draw on top of a canvas. Order matters!
		'''
		biome = self.get_biome(biome_ovr)
		self.biome = biome
		self.city_name = getCityName()

		if biome == ('tundra') or (biome == 'desert'):
			self.text_color = 'black'
		else:
			self.text_color = 'white'

		# set base img size
		self.imgx = 600
		self.imgy = self.imgx
		# initilize the image
		self.im = Image.new('RGBA',(self.imgx,self.imgy),'limegreen')
		self.draw = ImageDraw.Draw(self.im)

		# start drawing on top of the image
		self.draw_biome(biome)
		self.draw_water(biome)
		#self.draw_terrain()
		self.draw_flora(biome)

		city_dic = self.draw_city()
		self.town_names = self.draw_smalls()#camp_dic + vil_dic
		self.town_names.append(city_dic)


	def get_biome(self, override):

		if override != None:
			print "mapGen: biome is %s (override)" %override
			return override.lower()

		biomeLeanVal = (('marsh' ,1.0),('plains'  ,5.0),
						('hills' ,1.5),('tundra'  ,1.0),
						('desert',2.0),('forest'  ,3.0))
		biome = wChoice(biomeLeanVal)
		print "mapGen: biome is %s" %biome
		return biome

	def draw_biome(self,biome):

		# new method for drawing biome, but my images are ugly D;
		image_to_paste = Image.open('data/sprites/%s_texture.png'%biome)
		y_paste = 0
		for y_row in xrange(0,5):
			for x_paste_interval in xrange(0,self.imgx):
				if x_paste_interval % 128 == int():
					self.im.paste(image_to_paste,
						(x_paste_interval,y_paste), image_to_paste)
			y_paste += 128

	def draw_city(self):

		x = random.randrange(10,self.imgx-50)
		y = random.randrange(10,self.imgy-50)
		image_to_paste = Image.open('data/sprites/city.png')
		self.im.paste(image_to_paste, (x,y), image_to_paste)
		self.draw.text((x-10,y+18),str(self.city_name), fill=self.text_color)
		self.city_location = (x,y)
		city_dic = {
			'Name':self.city_name,
			'Type':'Region Capital',
			'Distance':0,
			'click_area':self.city_location
					}
		return city_dic

	def draw_smalls(self):

		smalls_li = list()
		types = ['Cave','Village',
				'Camp','Temple']

		for TYPE in types:
			density = random.randint(1,5)
			image_to_paste = Image.open('data/sprites/'+TYPE.lower()+'.png')
			for c in xrange(0,density):
				name = getSmallName(TYPE)
				x = random.randrange(10,self.imgx-50)
				y = random.randrange(10,self.imgy-50)
				self.im.paste(image_to_paste, (x,y), image_to_paste)
				self.draw.text((x-10,y+18),'%s'%name, fill=self.text_color)
				roadLength = int(gridDistance((self.city_location,(x,y))) / 15) # to be used for km
				self.draw.text((x-10,y+25),'to city: %dkm'%(roadLength), fill=self.text_color)
				smallsDat = {
				'Type':TYPE,
				'Name':name,
				'Distance':str(roadLength),
				'click_area':[x,y],
				}
				smalls_li.append(smallsDat)
		return smalls_li

	def draw_terrain(self):

		def draw_scorch_marks():
			density = random.randint(0,9)
			if density > 2:
				for c in xrange(0,density):
					x = random.randrange(10,self.imgx-50)
					y = random.randrange(10,self.imgy-50)
					image_to_paste = Image.open('data/sprites/scorch_texture.png')
					self.im.paste(image_to_paste, (x,y), image_to_paste)



		def hills():
			density = random.randint(1,3)
			for c in xrange(0,density*100):
				x = random.randint(0,self.imgx)
				y = random.randint(0,self.imgy)
				self.draw.arc((x,y,x+20,y+20),220,340, fill='gray')

		draw_scorch_marks()

	def draw_water(self, biome):

		def river(densityFactor):

			density = random.randint(0,4)
			streamCount = int(density + (density*densityFactor))
			for c in xrange(0,streamCount):
				# determines whether to start on x or y axis
				dir_num = random.randint(4,9)
				if random.choice((True,False)):
					x = random.randrange(0,self.imgx)
					y = 0
				else:
					x = 0
					y = random.randrange(0,self.imgy)
				for null in xrange(0,10000):
					# decides which direction to wander
					if random.choice((True,False)):
						if random.randint(0,random.randint(5,9)) < random.randint(0,9):
							x -= 1
						else:
							x += 1
						if (x >= self.imgx):
							break
					else:
						if random.randint(0,dir_num) < random.randint(0,random.randint(5,9)):
							y -= 1
						else:
							y += 1
						if (y >= self.imgy):
							break
					self.draw.point((x,y), fill='#2A2CD8')
					self.draw.point((x-1,y-1), fill='navy')
					self.draw.point((x+1,y+1), fill='navy')

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


		# Tree intensity Modifiers
		tree_mod ={
		'forest':[random.randint(2,4),('tree1','tree2')],
		'plains':[0.5,	('tree3','desertF1')],
		'hills':[0.5,	('tree3','desertF1')],
		'tundra':[0.2,	('tree3','desertF1')],
		'marsh':[1,		('marshF1','tree2')],
		'desert':[0.1,	('desertF1','desertF2')]
		}

		trees(tree_mod[biome][0],tree_mod[biome][1])

	def save_image(self):
		self.im.save('landMap', "PNG")

	def show_image(self):
		self.im.show()


class Town_Image(Land_Image):

	'''
	All data needed to create a new image representing a Town-generated
	area.
	'''

	def __init__(self, pref):

		self.settings = pref

		#get cityname from Land_Image
		self.city_name = landImg.city_name

		self.towns = self.populate_area()
		self.imgx = 600
		self.imgy = self.imgx
		# initilize the image
		self.im = Image.new('RGB',(self.imgx,self.imgy),'lightgray')
		# lets not draw things until it's ready
		#self.draw = ImageDraw.Draw(self.im)
		#self.drawStreets()
		#self.drawWalls()

	def populate_area(self):

		city_list = list()
		for city_dicts in landImg.town_names:
			cities = dict()

			cities['Name'] = city_dicts['Name']
			cities['Type'] = city_dicts['Type']
			cities['Distance'] = city_dicts['Distance']
			cities['click_area'] = city_dicts['click_area']
			if city_dicts['Type'] == "Region Capital":
				city_data = townGen.main('big',landImg.biome, self.settings)
				cities['Data'] = city_data
			else:
				town_data = townGen.main('small',landImg.biome, self.settings)
				cities['Data'] = town_data
			city_list.append(cities)
		return city_list

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
		self.city_name = landImg.city_name
		self.imgx = 600
		self.imgy = self.imgx
		# initilize the image
		self.im = Image.new('RGB',(self.imgx,self.imgy),'maroon')
		self.draw = ImageDraw.Draw(self.im)


	def save_image(self):
		self.im.save('landMap', "PNG")

	def show_image(self):
		self.im.show()

def main(opt, pref):
	global landImg, townImg, bldgImg
	if opt == 'tk':
		landImg = Land_Image(pref['map']['Biome'])
		townImg = Town_Image(pref)
		#bldgImg = Building_Image()
		return (landImg.im, landImg.city_name,
			townImg.towns)
	if opt == 'small':
		pass
	else:
		landImg = Land_Image(pref['map']['Biome'])
		townImg = Town_Image(pref)
		bldgImg = Building_Image()
		#townImg.show_image()

		return 0

if __name__ == '__main__':
	char_setting = {
		'use':False,
		'Level':random.randint(1,3),
		'Class':'Commoner',
		'Race':None,
			}

	map_setting = {
				'Biome':None,
				}
	town_settings = {
				'size_mod': 1.0
				}

	default_settings = {
			'char':char_setting,
			'map':map_setting,
			'town':town_settings
					}
	main('', default_settings)

