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
        affluence = self.get_affluence()
        govt = self.get_govt(affluence)
        econ_system = self.get_economy(affluence, govt)
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
        
        political_systems = {
            0.8:'Anarchism',
            1.2:'City-state',
            1.0:'Democracy',
            1.4:'Federacy',
            0.7:'Feudalism',
            0.5:'Authoritarian state',
            1.6:'Directorialism',
            1.7:'Meritocracy',
            0.8:'Monarchy',
            0.4:'Theocracy',
            }

        power_structure = None
        power_source = None
        
        closest_num = min(political_systems.keys(), key=lambda x:abs(x-affluence))
        return political_systems[closest_num]

    def get_affluence(self):
        aff = self.settings['town']['affluence']
        
        #use bonus
        if bool(random.getrandbits(1)):
            #positive
            if bool(random.getrandbits(1)):
                aff += random.random()
            else:
                aff -= random.random()
        
        if aff <= 0.0:
            aff = 0.1
        
        return aff

    def get_clans(self):
        pass

    def get_laws(self, govt):
        pass
        
    def get_wares(self, affluence):
        pass
    
    def get_economy(self, affluence, govt):
        
        political_systems = {
            'Anarchism':('Anarchist','Corporatist','Georgist'),
            'City-state':('Capitalist','Corporatist','Participatory','Mercantilist'),
            'Democracy':('Capitalist','Laissez-faire','Mercantilist'),
            'Federacy':('Capitalist','Georgist','Mercantilist'),
            'Feudalism':('Protectionist','Mercantilist'),
            'Authoritarian state':('State capitalist','Mercantilist'),
            'Directorialism':('Communist','Laissez-faire'),
            'Meritocracy':('Communist','Laissez-faire','Market socialist'),
            'Monarchy':('Protectionist','Mercantilist'),
            'Theocracy':('Communist','Georgist','Market socialist'),
            }
        
        # Took descriptions from child articles from https://en.wikipedia.org/wiki/Economic_system
        economic_systems = {
            'Anarchist'     :"The system of specialization in the various crafts, which would lead to a man's following the task for which he had the greatest aptitude, and distributing his surplus products to whoever may need them, receiving what he himself needs of other things from the surplus produced by his neighbours, but always on the basis of free distribution, not of exchange.",
            'Capitalist'    :"System in which trade, industry, and the means of production are largely or entirely privately owned. Private firms and proprietorships usually operate in order to generate profit, but may operate as private nonprofit organizations.",
            'Communist'     :"Characterized by common ownership of the means of production with free access to the articles of consumption and is classless and stateless, implying the end of the exploitation of labor.",
            'Corporatist'   :"Sociopolitical organization of a society by major interest groups, or corporate groups, such as agricultural, business, ethnic, labour, military, patronage, or scientific affiliations, on the basis of common interests.",
            'Georgist'      :"The economic value derived from natural resources and natural opportunities should belong equally to all residents of a community, but that people own the value they create.",
            'Laissez-faire' :"An economic system in which transactions between private parties are free from government interference such as regulations, privileges, tariffs, and subsidies.",
            'Market socialist':"A type of economic system involving the public, cooperative or social ownership of the means of production in the framework of a market economy. Market socialism differs from non-market socialism in that the market mechanism is utilized for the allocation of capital goods and the means of production.",
            'Mercantilist'  :"Promotes governmental regulation of a nation's economy for the purpose of augmenting state power at the expense of rival national powers. Mercantilism includes a national economic policy aimed at accumulating monetary reserves through a positive balance of trade, especially of finished goods.",
            'Participatory' :"An economic system based on participatory decision making as the primary economic mechanism for the allocation of the factors of production and guidance of production in a given society. Participatory economics is a form of decentralized economic planning and socialism involving the common ownership of the means of production.",
            'Protectionist' :"The economic policy of restraining trade between states (countries) through methods such as tariffs on imported goods, restrictive quotas, and a variety of other government regulations designed to allow (according to proponents) fair competition between imports and goods and services produced domestically.",
            'State capitalist':"Commercial economic activity is undertaken by the state, where the means of production are organized and managed as business enterprises, including the processes of capital accumulation, wage labor, and centralized management.",
            }
            
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

