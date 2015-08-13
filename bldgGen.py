#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  bldgGen.py
#
#  Copyright 2014 Tyler Dinsmoor <pappad@airmail.cc>
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
# gets information provided from landGen to decide building construction
# passes info to townGen, which then makes a lot of buildings

try:
    import random
    import charGen
    import itemGen
except ImportError:
    print "You are missing essential Libraries. See README.md"
    exit()

def wChoice(wCh):
    import random
    '''must be in format: wChoice(('a',1.0),('b',2.0),('c',3.0))'''
    totalChoice = sum(w for c, w in wCh)
    random_uniform = random.uniform(0, totalChoice)
    upto = 0
    for c, w in wCh:
        if upto + w > random_uniform:
            return c
        upto += w
    assert False, "Shouldn't get here"

class Building(object):
    '''
    Facilitates the population of itself, passes data to townGen
    '''
    def __init__(self, biome, pref):
        self.settings = pref

        self.bldgDat = dict()
        self.bldgDat['Rooms'] = {}
        self.bldgDat['Purpose'], self.bldgDat['Rooms'] = self.get_rooms(random.randint(1,3))
        try:
            owner = random.choice(self.bldgDat['Rooms'][0]['Actors'].values())
        except IndexError:
            owner = "Community"
        self.bldgDat['Name'] = owner['First Name']+"'s %s"%self.bldgDat['Purpose']


    def get_rooms(self, rooms):

        d = {
            'Shack':['Entry','Kitchen','Common Area'],

            'Residence':['Entry','Kitchen','Living Area','Dining Area',
                'Common Area', 'Sleeping Quarters'],

            'General Store':['Entry','Store Room', 'Counter'],

            'Armory':['Entry','Forge', 'Counter'],

            'Farm':['Gate','Barn','Slaughter Room'],

            'Weapon Forge':['Entry','Forge', 'Counter',
                'Grinding Wheel'],

            'Tavern':['Entry','Kitchen','Social Area', 'Harlot Room'],

            'Inn':['Entry','Kitchen',
                'Common Area', 'Sleeping Quarters']
            }

        purpose = random.choice(d.keys())
        roomTypes = d[purpose]
        roomDat = list()
        for room in roomTypes:
            roomDat.append({
            'Actors':self.get_inhabitants(random.randint(1,5)),
            'Weapons':self.get_random_items('wep',random.randint(0,2)),
            'Armor':self.get_random_items('arm',random.randint(0,2)),
            'Type':room,
            })
        # needs to return list
        return purpose, roomDat

    def get_random_items(self, typ, amount):
        item_l = list()
        if typ == 'wep':
            for x in xrange(0,amount):
                item_l.append(itemGen.main('wep', 'rnd'))
        elif typ == 'arm':
            for x in xrange(0,amount):
                item_l.append(itemGen.main('arm', 'rnd'))
        return item_l

    def get_inhabitants(self, popul):
        inhabitants = dict()
        for inhabitant in xrange(0,popul):
            if random.choice((True, True, False)):
                char_setting = {
                    'use':True,
                    'Level':random.randint(1,3),
                    'Class':'Commoner',
                    'Race':None,
                        }
                settings = {
                        'char':char_setting
                            }
                person = charGen.custom_param(settings)
            else:
                person = charGen.custom_param(self.settings)

            key_name = person['Name']
            inhabitants[key_name] = person
        return inhabitants

def main(opt, biome, pref):
    '''
    Used to interface with townGen.
    '''

    if opt == 'town':
        bldg = Building(biome, pref)
        return bldg.bldgDat
    else:
        bldg = Building('forest', pref)
        return 0

if __name__ == '__main__':
    import def_settings
    default_settings = def_settings.get_def_settings()
    main(None,None, default_settings)

