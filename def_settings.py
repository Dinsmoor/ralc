#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  def_settings.py
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

import random

def get_def_settings():
	char_setting = {
		'use':False,
		'Level':random.randint(1,3),
		'Class':'Commoner',
		'Race':None,
			}

	map_setting = {
				'biome':None,
				}
	town_settings = {
				'size_mod': 1.0,
				'affluence':1.0,
				'govt':None,
				}

	default_settings = {
			'char':char_setting,
			'map':map_setting,
			'town':town_settings
					}
	return default_settings

