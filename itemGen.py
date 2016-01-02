#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  itemGen.py
#
#  Copyright 2015 Tyler Dinsmoor <pappad@airmail.cc>


try:
    import random
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
    weapon_list = list()
    #Name,attack roll, damage type, weapon class, weapon type, str req, dex req, int req
    for wep in wepdata: # every list in this list of lists
        weapon_list.append([ {
            'name':wep[0],
            'hit_die':wep[1],
            'damage_type':wep[2],
            'weapon_class':wep[3],
            'weapon_type':wep[4],
            }])
    return weapon_list

def load_armor():
    armdata = import_weapon_file('data/equipment/armor')
    armor_list = list()
    #name,type,cost,AC
    for arm in armdata:
        armor_list.append([{
        'name':arm[0],
        'type':arm[1],
        'cost':arm[2],
        'ac':arm[3],
        }])
    return armor_list

def rand_armor():
    armor = load_armor()
    rnd_arm = random.randint(0,len(armor)-1)
    for data in armor[rnd_arm]:
        return data

def rand_weapon():
    weapons = load_weapons() #list
    rnd_wep = random.randint(0,len(weapons)-1)
    for data in weapons[rnd_wep]:
        return data

def rand_item():
    itms = load_weapons() + load_armor()
    rnd_itm = random.randint(0,len(itms)-1)
    for data in itms[rnd_itm]:
        return data

def main(opt, item):
    '''
    Used to interface with townGen.
    '''

    if opt == 'wep':
        if item == 'rnd':
            return rand_weapon()
        elif item == 'all':
            return load_weapons()
    if opt == 'arm':
        if item == 'rnd':
            return rand_armor()
        elif item == 'all':
            return load_armor()
    else:
        print rand_weapon()
        print rand_armor()
        return 0

if __name__ == '__main__':
    main(None, None)
