#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  monGen.py
#
#  Copyright 2016 Tyler Dinsmoor <pappad@airmail.cc>
#

import random
import csv


class Encounter:
    def __init__(self, parent, montype='humanoid'):
        self.party = parent.settings['party']
        self.montype = montype

        mons, mons_xp, xp_thresh = self.encounter_build()
        
        self.mondesc = "%d/%d\nNAME | XP\n"%(mons_xp, xp_thresh)
        for m in mons:
            self.mondesc += m['name'] + m['xp'] + "\n"
        
    def get_xp_threshold(self, diff=1):
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

        for cha,lvl in self.party.iteritems():
            xp_total += lvl_diff[lvl][diff]
            cha_total += 1


        return xp_total

    def encounter_mult(self, mon_count, party_count):
        mon_mults = dict()
        mon_mults[1] = 1
        mon_mults[2] = 1.5
        for i in range(3,7):
            mon_mults[i] = 2
        for i in range(7,11):
            mon_mults[i] = 2.5
        for i in range(11,15):
            mon_mults[i] = 3

        if mon_count >= 15:
            mon_mult = 4
        else:
            mon_mult = mon_mults[mon_count]
        multlist = [0.5,1,1.5,2,2.5,3,4,5]

        mon_mult_pos = multlist.index(mon_mult)
        if party_count < 3:
            return multlist[mon_mult_pos-1]
        elif party_count >= 6:
            return multlist[mon_mult_pos+1]
        else:
            return multlist[mon_mult_pos]

    def encounter_build(self):
        xp_thresh = self.get_xp_threshold(3)
        mons = []
        mons_xp = 0

        monlist = Monster().monlist
        #self.montype = random.choice(('humanoid','monstrosity','beast','undead','construct','fiend','plant'))
        
        futility_counter = 0
        while mons_xp <= xp_thresh - (xp_thresh*0.25):
            cur_mon = random.choice(monlist)
            if self.montype not in cur_mon['type']:
                continue
            futility_counter += 1
            if futility_counter > 2000:
                break
            mons.append(cur_mon)

            def recalc_xp():
                mons_xp = 0
                for mon in mons:
                    mons_xp += int(mon['xp'].replace(',',''))
                mons_xp_mod = self.encounter_mult(len(mons), len(self.party))
                mons_xp = mons_xp_mod * mons_xp
                return mons_xp
            mons_xp = recalc_xp()

            if mons_xp >= ((xp_thresh) + (xp_thresh*0.1)):
                try:
                    #print "REMVOING",mons[-1]['name']
                    del mons[-1]
                except KeyError:
                    pass
                if mons == []:
                    mons_xp = 0
                    continue
                mons_xp = recalc_xp()

        print mons_xp,"/", xp_thresh
        
        return mons, mons_xp, xp_thresh

class Monster:
    monlist = list()
    def __init__(self):
        self.build_monlist()
        self.mon = random.choice(self.monlist)
        self.mon_desc = self.desc_mon(self.mon)

    def build_monlist(self):
        with open('data/monsters.csv', 'rb') as f:
            monreader = csv.DictReader(f, delimiter=';')
            for row in monreader:
                #name;type;alignment;ac;armor_type;hit_points;hit_die;
                #speed;str;dex;con;int;wis;cha;save_throws;skills;
                #dam_resist;dam_immune;cond_immune;senses;language;
                #challenge;xp;none;actions;leg_actions;abilities
                self.monlist.append(row)
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
