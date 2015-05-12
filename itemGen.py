#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  itemGen.py
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
	import random
	from libdndGen import *
except ImportError:
	print "You are missing essential Libraries. See README.md"
	exit()

class Item(object):


    def __init__(self,name="Generic Item",
                str_bonus=0, dex_bonus=0, int_bonus=0,
                hit=None, wep_type=None, wep_class=None,
                dam_type=None, defend=0,
                key_level=0):

        self.name = name
        self.str_bonus = str_bonus
        self.dex_bonus = dex_bonus
        self.int_bonus = int_bonus
        self.hit = hit
        self.wep_type = wep_type
        self.defend = defend
        self.keylevel = key_level


    def describe_item(self):
        print '''
Name: %s
Attributes:
    TYP: %s
    HIT: %s
    DEF: %d
    KEY: %d
        '''%(self.name,
            self.wep_type,self.hit,self.defend,self.keylevel)
##########
weapon_dict = {}

def import_weapon_file(fi):
	fi = open(fi)
	# Builds a list of lists from a file, seperated by newline
	li = [i.strip().split(',') for i in fi.readlines() if not i.startswith("#")]
	# ignore blank lines
	li = [x for x in li if x != ['']]
	li = [[st.strip() for st in l] for l in li]
	fi.close()
	return li

def load_weapons():
	wepdata = import_weapon_file('data/equipment/weapons')
	#Name,attack roll, damage type, weapon class, weapon type, str req, dex req, int req
	for wep in wepdata:
		weapon_dict[wep[0]] = Item(name=wep[0],hit=wep[1],
				wep_type=wep[2], wep_class=wep[3], dam_type=wep[4])
	


def main(opt, item):
	'''
	Used to interface with townGen.
	'''

	if opt == 'wep':
		
		bldg = Building(biome)
		return bldg.bldgDat
	else:
		load_weapons()
		for name, item in weapon_dict.iteritems():
			item.describe_item()
		return 0

if __name__ == '__main__':
	main(None, None)

