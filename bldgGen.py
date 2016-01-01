#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  bldgGen.py
#
#  Copyright 2014 Tyler Dinsmoor <pappad@airmail.cc>
#

try:
    import random
    #import charGen
    import npcGen
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
        self.bldgDat['Actors'] = {}
        self.bldgDat['Purpose'], self.bldgDat['Actors'] = self.get_actors()
        try:
            owner = random.choice(self.bldgDat['Actors'].keys())
        except IndexError:
            owner = "Community"
        self.bldgDat['Name'] = owner+"'s %s"%self.bldgDat['Purpose']


    def get_actors(self):

        types = (('Shack',20),('Residence',50),('General Store',10),
                ('Armory',5),('Farm',5),('Weapon Forge',5),
                ('Tavern',5),('Inn',10),('Hardware Store',5),
                ('Woodsmith',5))

        d = {
            'Shack':4,
            'Residence':4,
            'General Store':7,
            'Armory':5,
            'Farm':14,
            'Weapon Forge':7,
            'Tavern':20,
            'Inn':25,
            'Hardware Store':7,
            'Woodsmith':10,
            }


        purpose = wChoice(types)
        
        actors = self.get_inhabitants(random.randint(3,d[purpose]))
        return purpose, actors

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
            npc = npcGen.NPC()
            person = npc.desc
            #if random.choice((True, True, False)):
                #char_setting = {
                    #'use':True,
                    #'Level':random.randint(1,3),
                    #'Class':'Commoner',
                    #'Race':None,
                        #}
                #settings = {
                        #'char':char_setting
                            #}
                #person = charGen.custom_param(settings)
            #else:
                #person = charGen.custom_param(self.settings)

            key_name = npc.npcinfo['name']
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

