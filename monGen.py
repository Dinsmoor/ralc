#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  monGen.py
#  
#  Copyright 2016 Tyler Dinsmoor <pappad@airmail.cc>
#  

import random
import csv

class Monster:
    monlist = list()
    def __init__(self):
        self.build_monlist()
        self.mon =self.rand_mon()
        self.mon_desc = self.desc_mon(self.mon)
    
    def build_monlist(self):
        with open('data/monsters.csv', 'rb') as f:
            monreader = csv.DictReader(f, delimiter=';')
            for row in monreader:
                #name;type;alignment;ac;armor_type;hit_points;hit_die;speed;str;dex;con;int;wis;cha;save_throws;skills;dam_resist;dam_immune;cond_immune;senses;language;challenge;xp;none;actions;leg_actions;abilities
                self.monlist.append(row['name'])
                #print row[0],row[26]
    
    def rand_mon(self):
        mon = random.choice(self.monlist)
        with open('data/monsters.csv', 'rb') as f:
            monreader = csv.DictReader(f, delimiter=';')
            for row in monreader:
                if row['name'] == mon:
                    return row
    
    def desc_mon(self, mr):
        mondesc = """
Name: %s
Challenge:%s XP:%s
Type:%s
Align:%s
AC:%s Armor:%s
HP:%s Hit Die:%s
Speed:%s
STR DEX CON INT WIS CHA
%s %s %s %s %s %s
Saving throws:%s
Skills:%s
Damage Resistances:%s
Damage Immunities:%s
Condition Immunities:%s
Senses:%s
Language:%s

Actions:%s

Legendary Actions:%s

Abilities:%s
"""%(mr['name'],mr['challenge'],mr['xp'],mr['type'],mr['alignment'],
    mr['ac'],mr['armor_type'],mr['hit_points'],mr['hit_die'],mr['speed'],
    mr['str'],mr['dex'],mr['con'],mr['int'],mr['wis'],mr['cha'],
    mr['save_throws'],mr['skills'],mr['dam_resist'],mr['dam_immune'],
    mr['cond_immune'],mr['senses'],mr['language'],mr['actions'].replace('<br>','\n'),
    mr['leg_actions'].replace('<br>','\n'),mr['abilities'].replace('<br>','\n'))
        return mondesc
