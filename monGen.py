#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  monGen.py
#
#  Copyright 2016 Tyler Dinsmoor <pappad@airmail.cc>
#

import random
import csv

# 'chars' example data
exmp_party = [{'name':'Bobby', 'lvl':5}, {'name':'Billy', 'lvl':5}, {'name':'Bo', 'lvl':5}]

class Encounter:
    def __init__(self, chars=exmp_party):
        self.party = chars
        
        self.encounter_build()

    def get_xp_threshold(self, diff=0):
        lvl_diff = {
            #lvl: easy, medium, hard, deadly
            1:((25),(50),(75),(100)),
            2:((50),(100),(150),(200)),
            3:((75),(150),(225),(400)),
            4:((125),(250),(375),(500)),
            5:((250),(500),(750),(1100)),
            6:((300),(600),(900),(1400)),
            7:((350),(750),(1100),(1700)),
            8:((450),(900),(1400),(2100)),
            9:((550),(1100),(1600),(2400)),
            10:((600),(1200),(1900),(2800)),
            11:((800),(1600),(2400),(3600)),
            12:((1000),(2000),(3000),(4500)),
            13:((1100),(2200),(3400),(5100)),
            14:((1250),(2500),(3800),(5700)),
            15:((1400),(2800),(4300),(6400)),
            16:((1600),(3200),(4800),(7200)),
            17:((2000),(3900),(5900),(8800)),
            18:((2100),(4200),(6300),(9500)),
            19:((2400),(4900),(7300),(10900)),
            20:((2800),(5700),(8500),(10700)),
                    }
        
        xp_total = 0
        cha_total = 0
        
        for cha in self.party:
            xp_total += lvl_diff[cha['lvl']][diff]
            cha_total += 1
        
        
        return xp_total

    def encounter_mult(self, mon_count, party_count):
        mon_mults = {
            (1):1,
            (2):1.5,
            (3,4,5,6):2,
            (7,8,9,10):2.5,
            (11,12,13,14):3
                    }
        for k,v in mon_mults.iteritems():
            if mon_count >= 15:
                mon_mult = 4
            elif mon_count in k:
                mon_mult = v
        multlist = [0.5,1,1.5,2,2.5,3,4,5]

        mon_mult_pos = multlist.index(mon_mult)
        if party_count < 3:
            return multlist[mon_mult_pos-1]
        elif party_count >= 6:
            return multlist[mon_mult_pos+1]
    
    def type_select(self):
        types = ('humanoid','monstrosity','beast','undead','construct','fiend','plant')
    
    def encounter_build(self):
        xp_thresh = self.get_xp_threshold(2)
        mons = []
        mons_xp = 0
        
        while mons_xp <= xp_thresh - (xp_thresh*0.1):
            cur_mon = Monster().mon
            mon_xp = int(cur_mon['xp'].replace(',',''))
            if (mon_xp < xp_thresh) and (mons_xp+mon_xp < xp_thresh):
                
                mons.append(cur_mon)
                mons_xp += mon_xp
        
        print mons_xp, xp_thresh
        
        for mon in mons:
            print mon['name'], mon['xp'], mon['type'].lower()
            
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
                #name;type;alignment;ac;armor_type;hit_points;hit_die;
                #speed;str;dex;con;int;wis;cha;save_throws;skills;
                #dam_resist;dam_immune;cond_immune;senses;language;
                #challenge;xp;none;actions;leg_actions;abilities
                self.monlist.append(row['name'])
                #print row[0],row[26]
            f.close()

    def rand_mon(self):
        mon = random.choice(self.monlist)
        with open('data/monsters.csv', 'rb') as f:
            monreader = csv.DictReader(f, delimiter=';')
            for row in monreader:
                if row['name'] == mon:
                    return row
        f.close()

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

Encounter()
