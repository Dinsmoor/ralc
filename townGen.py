#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  townGen.py
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
#  responsible for making buildings, and doing logic for deciding how
#  many buildings there will be, will pass info to civGen, and then
#  use that data for populatng city
try:
    import random
    import bldgGen
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

def getFromFile_LoL(fi):
    fi = open(fi)
    # Builds a list of lists from a file, seperated by newline
    li = [i.strip().split(',') for i in fi.readlines() if not i.startswith("#")]
    # ignore blank lines
    li = [x for x in li if x != ['']]
    li = [[st.strip() for st in l] for l in li]
    fi.close()
    return li

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
def getStreetName():
    import random
    streetName = random.choice(getFromFile_T('data/streets'))
    for s in streetName:
        return s

class Settlement(object):
    def __init__(self, biome, pref):
        self.settings = pref
        #affluence = self.get_affluence()
        #govt = self.get_govt(affluence)
        #senses = self.get_senses(affluence, govt)
        citySize = self.getCitySize(biome)
        self.s = self.getStreets(citySize, biome)

    def parse_settings(self):
        self.settings['town']['size_mod']

    def getBldgData(self, biome):
        return bldgGen.main('town', biome, self.settings)

    def getCitySize(self, biome):
        # city size multipliers
        size_mult ={
            'forest':1.0,
            'plains':0.7,
            'hills':0.7,
            'tundra':0.3,
            'marsh':0.5,
            'desert':0.2,
            'small':0.2,
            }
        mult = size_mult[biome]
        if self.settings['town']['size_mod'] != 1.0:
            mult = mult * self.settings['town']['size_mod']

        return int(mult * (random.randint(1,4) + 10))

    def get_govt(self, affluence):

        d = {
            1.0:'Democracy'
            }

        govt = d[affluence]
        return govt

    def get_affluence(self):
        aff = self.settings['town']['affluence']

        return aff

    def get_clans(self):
        pass

    def get_laws(self, govt):
        pass
        
    def get_wares(self, affluence):
        pass
    
    def get_economy(self, govt, affluence):
        pass
        
    def get_description(self):
        pass

    def get_senses(self, affluence, govt):

        senses = getFromFile_LoL('data/senses')
        affluence = 'poor'
        d = {
            'poor':(0,1,2,3,4,5),
            'average':(6,7,8,9,10,11),
            'affluent':(12,13,14,15,16,17),
            'rich':(18,19,20,21,22,23),
            }

        senses_filtered = list()
        for sense in d[affluence]:
            senses_filtered.append(senses[sense])

        smell_des = "You smell %s. You would describe the town's smell as %s.\n"%(
            random.choice(senses_filtered[0]),
            random.choice(senses_filtered[1]))
        sight_des = "You see %s. You would describe the town's signts as %s.\n"%(
            random.choice(senses_filtered[2]),
            random.choice(senses_filtered[3]))
        sound_des = "You hear %s. You would describe the town's sounds as %s.\n"%(
            random.choice(senses_filtered[4]),
            random.choice(senses_filtered[5]))
        desc = smell_des+sight_des+sound_des
        print desc
        return desc

    def getStreets(self, citySize, biome):
        streets = dict()
        for val in xrange(0,citySize):
            streets[getStreetName()] = self.fillStreet(biome, citySize)
        return streets

    def fillStreet(self, biome, citySize):
        lotCount = random.randint(1,4) + citySize
        bldgList = []
        for lot in xrange(0,lotCount):
            bldgList.append(self.getBldgData(biome))
        return bldgList

def main(opt, biome, pref):
    if opt == 'big':
        town = Settlement(biome, pref)
        return town.s
    if opt == 'small':
        town = Settlement('small', pref)
        return town.s
    else:
        town = Settlement('forest', pref)
        return 0

if __name__ == '__main__':
    import def_settings
    default_settings = def_settings.get_def_settings()
    main(None,None, default_settings)

