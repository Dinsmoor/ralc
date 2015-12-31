#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  charGen.py
#
#  Copyright 2014 Tyler Dinsmoor <pappad@airmail.cc>


try:
    import random
    import argparse
    import itemGen
    from markovnames import nameGen
except ImportError:
    print "You are missing essential Libraries. See README.md"

racesTup = ('Human', 'Elf', 'Dwarf', 'Halfling', 'Half-Elf', 'Half-Orc',
            'Dragonborn', 'Gnome')
classesTup = ('Cleric', 'Druid', 'Ranger', 'Paladin', 'Warlock', 'Wizard',
              'Barbarian', 'Fighter', 'Rouge', 'Monk', 'Bard', 'Sorcerer')


def weighted_choice(wCh):
    """

    :rtype : single weighted item
    """
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


def maxi(l):
    m = max(l)
    for i, v in enumerate(l):
        if m == v:
            return i


def mini(l):
    m = min(l)
    for i, v in enumerate(l):
        if m == v:
            return i


def get_f_f_lol(fi):
    """

    :rtype : List of Lists
    """
    fi = open(fi)
    # Builds a list of lists from a file, separated by newline
    li = [i.strip().split(',') for i in fi.readlines() if not i.startswith("#")]
    # ignore blank lines
    li = [x for x in li if x != ['']]
    li = [[st.strip() for st in l] for l in li]
    fi.close()
    return li


def get_f_f_dic(fi):
    d = {}
    with open(fi) as f:
        for line in f:
            if not line.startswith("#"):
                (key, val) = line.strip().split('=')
                d[key] = val
    return d


def get_background_list(fi):
    fi = open(fi)
    # Builds a list of lists from a file, separated by newline
    li = [i.strip().split('::') for i in fi.readlines() if not i.startswith("#")]
    # ignore blank lines
    li = [x for x in li if x != ['']]
    li = [[st.strip() for st in l] for l in li]
    fi.close()
    return li


def force_class(pc_class):
    """
    Inefficient way of forcing a class, but since the stats are random,
    and need to go along with what sort of class you get, this is the way
    to do it.
    """
    global new_class
    low_class = pc_class.lower()
    low_new = new_class.lower()
    while low_class != low_new:
        pc_class = get_stats()
        low_class = pc_class.lower()
    return pc_class


def get_stats():
    """
    Gets both stats and class, should probably be broken up into separate
    functions, but works fine, really. Could be moved to main(), but that
    would just make main() more bloated, no need.
    """
    global pc
    pc['STR'] = get_stat_roll()
    pc['DEX'] = get_stat_roll()
    pc['CON'] = get_stat_roll()
    pc['INT'] = get_stat_roll()
    pc['WIS'] = get_stat_roll()
    pc['CHR'] = get_stat_roll()
    stat_tup = (pc['STR'], pc['DEX'], pc['CON'], pc['INT'], pc['WIS'], pc['CHR'])

    try:
        if stat_tup[0] == max(stat_tup):
            tup = (('Barbarian', 5), ('Fighter', 3), ('Paladin', 3))
        elif stat_tup[1] == max(stat_tup):
            tup = (('Rouge', 5), ('Ranger', 3), ('Monk', 3), ('Fighter', 3))
        elif stat_tup[2] == max(stat_tup):
            tup = (('Barbarian', 5), ('Fighter', 3), ('Sorcerer', 1))
        elif stat_tup[3] == max(stat_tup):
            tup = (('Wizard', 5), ('Rouge', 1), ('Druid', 1))
        elif stat_tup[4] == max(stat_tup):
            tup = (('Cleric', 5), ('Druid', 5), ('Ranger', 3),
                   ('Paladin', 1), ('Warlock', 1), ('Wizard', 1))
        elif stat_tup[5] == max(stat_tup):
            tup = (('Bard', 5), ('Sorcerer', 5), ('Warlock', 5),
                   ('Paladin', 3), ('Cleric', 1))
        return weighted_choice(tup)
    except:
        print "GETSTATS ERROR: DEFAULTING TO FIGHTER"
        return 'Fighter'


def get_stat_modifiers(st):
    """

    :rtype : stat_modifier
    """
    return st / 2 - 5


def get_stat_roll():
    """
    Meant to accurately emulate a 4d6d1
    """
    r1 = random.randint(1, 6)
    r2 = random.randint(1, 6)
    r3 = random.randint(1, 6)
    r4 = random.randint(1, 6)
    r_list = [r1, r2, r3, r4]
    r_list.pop(mini(r_list))
    return r_list[0] + r_list[1] + r_list[2]


def get_prof_level(level):
    """

    :rtype : pc['Level']
    """
    d = {
        (1, 2, 3, 4): 2,
        (5, 6, 7, 8): 3,
        (9, 10, 11, 12): 4,
        (13, 14, 15, 16): 5,
        (17, 18, 19, 20): 6,
    }

    for k, v in d.iteritems():
        if level in k:
            return v


def get_race_bonus(pc_race):
    """
    Easy, but ugly way to get bonuses per race, but since we have
    to use strings to compare things, this is the only way to go.
    Also, it may be better to make subrace in a different function, or even
    in getRace() itself, since this is messy.
    """
    global pc
    if pc_race == "Dwarf":
        sub_races = ('Mountain', 'Hill')
        pc['CON'] += 2
        pc['Traits'].append('Darkvision')
        pc['Traits'].append('Dwarven Resilience')
    elif pc_race == "Elf":
        sub_races = ('High', 'Wood', 'Dark')
        pc['DEX'] += 2
        pc['Traits'].append('Darkvision')
        pc['Traits'].append('Keen Senses')
        pc['Prof'].append('SK Perception')
        pc['Traits'].append('Fey Ancestry')
        pc['Traits'].append('Trance')
    elif pc_race == "Halfling":
        sub_races = ('Lightfoot', 'Stout')
        pc['DEX'] += 2
        pc['Traits'].append('Lucky')
        pc['Traits'].append('Brave')
        pc['Traits'].append('Halfling Nimbleness')
    elif pc_race == "Human":
        sub_races = ('Calishite', 'Chondathan', 'Shou', 'Damaran',
                     'Tethyrian', 'Illuskan', 'Turami', 'Mulan', 'Rashemi')
        pc['STR'] += 1
        pc['DEX'] += 1
        pc['CON'] += 1
        pc['INT'] += 1
        pc['WIS'] += 1
        pc['CHR'] += 1
    elif pc_race == "Dragonborn":
        sub_races = ('Black', 'Blue', 'Brass', 'Bronze', 'Copper',
                     'Gold', 'Green', 'Red', 'White', 'Silver')
        pc['STR'] += 2
        pc['CHR'] += 1
        pc['Traits'].append('Draconic Ancestry')
        pc['Traits'].append('Breath Weapon')
        pc['Traits'].append('Damage Resistance')
    elif pc_race == "Gnome":
        sub_races = ('Forest', 'Rock')
        pc['DEX'] += 1
        pc['Traits'].append('Darkvision')
        pc['Traits'].append('Gnome Cunning')
    elif pc_race == 'Half-Elf':
        sub_races = ''
        pc['CHR'] += 2
        pc['Traits'].append('Darkvision')
        pc['Traits'].append('Fey Ancestry')
        pc['Traits'].append('Skill Versitality')
        pc['Traits'].append('+1 Language')
    elif pc_race == 'Half-Orc':
        sub_races = ''
        pc['STR'] += 2
        pc['CON'] += 1
        pc['Traits'].append('Darkvision')
        pc['Traits'].append('Menacing')
        pc['Traits'].append('Relentless Endurance')
        pc['Traits'].append('Savage Attack')
        pc['Prof'].append('SK Intimidation')

    elif pc_race == 'Tiefling':
        sub_races = ''
        pc['INT'] += 1
        pc['CHR'] += 2
        pc['Traits'].append('Darkvision')
        pc['Traits'].append('Hellish Resistance')
        pc['Traits'].append('Infernal Legacy')
    else:
        sub_races = ''
    try:
        pc_subrace = random.choice(sub_races)
        get_subrace_bonus(pc_subrace)
    except:
        pc_subrace = ""
    return pc_subrace


def get_subrace_bonus(pc_subrace):
    """
    Just changes vars in global PC
    :rtype : None
    """
    global pc
    if pc_subrace == 'Hill':
        pc['WIS'] += 1
        pc['Traits'].append('Dwarven Toughness')
    elif pc_subrace == "Mountain":
        pc['STR'] += 2
        pc['Traits'].append('Dwarven Armor Training')
    elif pc_subrace == "High":
        pc['INT'] += 1
        pc['Traits'].append('Elf Weapon Training')
        pc['Traits'].append('+1 Cantrip')
        pc['Traits'].append('Extra Language')
    elif pc_subrace == "Wood":
        pc['WIS'] += 1
        pc['Traits'].append('Elf Weapon Training')
        pc['Traits'].append('Fleet of Foot')
        pc['Traits'].append('Mask of the Wild')
    elif pc_subrace == "Dark":
        pc['CHR'] += 1
        pc['Traits'].append('Superior Darkvision')
        pc['Traits'].append('Sunlight Sensitivity')
        pc['Traits'].append('Drow Magic')
        pc['Traits'].append('Drow Weapon Training')
    elif pc_subrace == 'Lightfoot':
        pc['CHR'] += 1
        pc['Traits'].append('Naturally Stealthy')
    elif pc_subrace == 'Stout':
        pc['CON'] += 1
        pc['Traits'].append('Stout Resilience')
    elif pc_subrace == 'Forest':
        pc['DEX'] += 1
        pc['Traits'].append('Natural Illusionist')
        pc['Traits'].append('Speak with Small Beasts')
    elif pc_subrace == 'Rock':
        pc['CON'] += 1
        pc['Traits'].append('Artificer’s Lore')
        pc['Traits'].append('Tinker')


def get_hitpoints(pc_class, pc_level, pc_subrace):
    """
    It's best to use a dictionary here, to avoid messy shit like
    what exists above. Unfortunately, that wouldn't work up there because
    of the varying data that gets changed. This cannot be any more efficient.
    """
    hp_bonus = 0
    try:
        hit_dies = {
            'Sorcerer': 6, 'Wizard': 6, 'Bard': 8,
            'Fighter': 10, 'Paladin': 10, 'Ranger': 10,
            'Barbarian': 12, 'Cleric': 8, 'Druid': 8,
            'Monk': 8, 'Rouge': 8, 'Warlock': 8
        }

        if pc_subrace == 'Hill':
            hp_bonus = 1

        hit_points = hit_dies[pc_class] + pc['conMod'] + hp_bonus

        if pc_level == 1:
            return hit_points

        for x in xrange(1, pc_level):
            hit_points = hit_points + random.randint(1, hit_dies[pc_class]) + pc['conMod'] + hp_bonus
        return hit_points
    except:
        return 1


def get_race(pc_class):
    """
    Very autistic way of representing slightly different tendencies based
    upon one variable, but I'm unaware of any other mathematical expression
    or method that would make this easier.
    """
    d = {
        "Fighter": (('Dwarf', 10), ('Elf', 5), ('Halfling', 5), ('Human', 25),
                    ('Dragonborn', 3), ('Gnome', 2), ('Half-Elf', 5), ('Half-Orc', 5),
                    ('Tiefling', 2)),
        "Ranger": (('Dwarf', 10), ('Elf', 15), ('Halfling', 5), ('Human', 25),
                   ('Dragonborn', 1), ('Gnome', 5), ('Half-Elf', 5), ('Half-Orc', 1),
                   ('Tiefling', 1)),
        "Barbarian": (('Dwarf', 15), ('Elf', 5), ('Halfling', 5), ('Human', 25),
                      ('Dragonborn', 3), ('Gnome', 1), ('Half-Elf', 2), ('Half-Orc', 10),
                      ('Tiefling', 3)),
        "Wizard": (('Dwarf', 5), ('Elf', 15), ('Halfling', 5), ('Human', 25),
                   ('Dragonborn', 2), ('Gnome', 8), ('Half-Elf', 10), ('Half-Orc', 1),
                   ('Tiefling', 2)),
        "Cleric": (('Dwarf', 5), ('Elf', 15), ('Halfling', 5), ('Human', 25),
                   ('Dragonborn', 2), ('Gnome', 2), ('Half-Elf', 10), ('Half-Orc', 2),
                   ('Tiefling', 2)),
        "Bard": (('Dwarf', 5), ('Elf', 15), ('Halfling', 15), ('Human', 25),
                 ('Dragonborn', 5), ('Gnome', 5), ('Half-Elf', 10), ('Half-Orc', 5),
                 ('Tiefling', 5)),
        "Druid": (('Dwarf', 5), ('Elf', 15), ('Halfling', 5), ('Human', 25),
                  ('Dragonborn', 2), ('Gnome', 2), ('Half-Elf', 7), ('Half-Orc', 5),
                  ('Tiefling', 2)),
        "Monk": (('Dwarf', 10), ('Elf', 10), ('Halfling', 5), ('Human', 25),
                 ('Dragonborn', 3), ('Gnome', 2), ('Half-Elf', 6), ('Half-Orc', 5),
                 ('Tiefling', 4)),
        "Paladin": (('Dwarf', 15), ('Elf', 5), ('Halfling', 5), ('Human', 25),
                    ('Dragonborn', 5), ('Gnome', 2), ('Half-Elf', 7), ('Half-Orc', 10),
                    ('Tiefling', 2)),
        "Rouge": (('Dwarf', 8), ('Elf', 20), ('Halfling', 10), ('Human', 25),
                  ('Dragonborn', 2), ('Gnome', 8), ('Half-Elf', 5), ('Half-Orc', 1),
                  ('Tiefling', 2)),
        "Sorcerer": (('Dwarf', 10), ('Elf', 10), ('Halfling', 10), ('Human', 25),
                     ('Dragonborn', 2), ('Gnome', 4), ('Half-Elf', 11), ('Half-Orc', 1),
                     ('Tiefling', 2)),
        "Warlock": (('Dwarf', 10), ('Elf', 10), ('Halfling', 10), ('Human', 25),
                    ('Dragonborn', 2), ('Gnome', 4), ('Half-Elf', 11), ('Half-Orc', 1),
                    ('Tiefling', 2))
    }
    return weighted_choice(d[pc_class])


def get_alignment(pc_race):
    d = {
        "Human": (('N', 5), ('CG', 2), ('CN', 2), ('CE', 1),
                  ('LG', 2), ('LN', 2), ('LE', 1), ('NE', 1), ('NG', 2)),
        "Dwarf": (('N', 20), ('CG', 10), ('CN', 50), ('CE', 5),
                  ('LG', 15), ('LN', 10), ('LE', 5), ('NE', 5), ('NG', 5)),
        "Halfling": (('N', 2), ('CG', 2), ('CN', 2), ('CE', 1),
                     ('LG', 20), ('LN', 2), ('LE', 2), ('NE', 2), ('NG', 2)),
        "Elf": (('N', 10), ('CG', 20), ('CN', 10), ('CE', 5),
                ('LG', 15), ('LN', 30), ('LE', 5), ('NE', 5), ('NG', 5)),
        "Dragonborn": (('N', 1), ('CG', 2), ('CN', 1), ('CE', 8),
                       ('LG', 35), ('LN', 1), ('LE', 1), ('NE', 2), ('NG', 2)),
        "Gnome": (('N', 15), ('CG', 20), ('CN', 2), ('CE', 1),
                  ('LG', 20), ('LN', 2), ('LE', 1), ('NE', 1), ('NG', 5)),
        "Half-Elf": (('N', 15), ('CG', 25), ('CN', 20), ('CE', 5),
                     ('LG', 25), ('LN', 20), ('LE', 7), ('NE', 5), ('NG', 15)),
        "Half-Orc": (('N', 10), ('CG', 15), ('CN', 5), ('CE', 20),
                     ('LG', 5), ('LN', 10), ('LE', 20), ('NE', 15), ('NG', 10)),
        "Tiefling": (('N', 8), ('CG', 15), ('CN', 15), ('CE', 15),
                     ('LG', 10), ('LN', 8), ('LE', 12), ('NE', 5), ('NG', 5)),
    }
    return weighted_choice(d[pc_race])


def get_name(pc_race, pc_gender):
    """
    This is a nice snippet. It looks for a filename corresponding with the
    race name in a particular syntax, then imports all sorts of different names
    based upon their index in a list of lists.
    """


    global pc
    try:
        names = get_f_f_lol('data/char/' + (pc_race.lower() + 'Names'))
        if pc_race == 'Half-Orc':
            # half-orcs don't have last names
            pc['Last Name'] = ''
        else:
            pc['Last Name'] = nameGen.get_name(names[2])
        if pc_gender == 'Male':
            pc['First Name'] = nameGen.get_name(names[0])
        else:
            pc['First Name'] = nameGen.get_name(names[1])
        pcName = pc['First Name'] + ' ' + pc['Last Name']
    except Exception as e:
        print e
        pcName = "ERR"
    return pcName


def get_spells(pc_class, pc_level):
    """
    Similar in build to getName(), however it uses a dict to find out
    how many spell slots a character can/will use, dependant on their level,
    and then returns a predetermined number of random spells as designated in
    their class spell file.
    However cool this is, it is not accurate with the DNDv5 book, for building
    a character that a player would use, it would need to simply return a set of
    known spells, based on level, and then list the amount of spell slots they would
    have. That is much simpler, but since this is meant for npcs, it doesn't matter.
    """
    if pc_level > 20:
        pc_level = 20
    # 'class':(cantrips,total spells,lvl1,lvl2,etc...)
    std_slots = {
        1: (2, 2),
        2: (2, 3),
        3: (2, 4, 2),
        4: (3, 4, 3),
        5: (3, 4, 3, 2),
        6: (3, 4, 3, 3),
        7: (3, 4, 3, 3, 1),
        8: (3, 4, 3, 3, 2),
        9: (3, 4, 3, 3, 3, 1),
        10: (4, 4, 3, 3, 3, 2),
        11: (4, 4, 3, 3, 3, 2, 1),
        12: (4, 4, 3, 3, 3, 2, 1),
        13: (4, 4, 3, 3, 3, 2, 1, 1),
        14: (4, 4, 3, 3, 3, 2, 1, 1),
        15: (4, 4, 3, 3, 3, 2, 1, 1, 1),
        16: (4, 4, 3, 3, 3, 2, 1, 1, 1),
        17: (4, 4, 3, 3, 3, 2, 1, 1, 1, 1),
        18: (4, 4, 3, 3, 3, 3, 1, 1, 1, 1),
        19: (4, 4, 3, 3, 3, 3, 2, 1, 1, 1),
        20: (4, 4, 3, 3, 3, 3, 2, 2, 1, 1),
    }
    cur_slots = std_slots[pc_level]
    try:
        spells = list()
        spell_lol = get_f_f_lol('data/char/' + (pc_class.lower() + 'Spells'))
        for spell in spell_lol:
            random.shuffle(spell)
        for s, l in zip(spell_lol, cur_slots):
            spells.append(s[0:l])
        return spells
    except Exception:
        return None


def get_skills(pc_race, pc_class):
    skills = {}
    if pc_race == "Dwarf":
        pass


def get_background(pc_class):
    d = {
        "Cleric": (('Acolyte', 25), ('Charlatan', 5),
                   ('Criminal', 5), ('Entertainer', 5), ('Folk Hero', 10),
                   ('Guild Artisan', 5), ('Hermit', 5), ('Noble', 10),
                   ('Outlander', 5), ('Sage', 15), ('Sailor', 5),
                   ('Soldier', 5), ('Urchin', 5)),
        "Druid": (('Acolyte', 20), ('Charlatan', 5),
                  ('Criminal', 5), ('Entertainer', 5), ('Folk Hero', 10),
                  ('Guild Artisan', 5), ('Hermit', 5), ('Noble', 10),
                  ('Outlander', 10), ('Sage', 20), ('Sailor', 5),
                  ('Soldier', 5), ('Urchin', 10)),
        "Ranger": (('Acolyte', 15), ('Charlatan', 15),
                   ('Criminal', 10), ('Entertainer', 10), ('Folk Hero', 15),
                   ('Guild Artisan', 10), ('Hermit', 5), ('Noble', 15),
                   ('Outlander', 10), ('Sage', 15), ('Sailor', 5),
                   ('Soldier', 15), ('Urchin', 10)),
        "Paladin": (('Acolyte', 20), ('Charlatan', 10),
                    ('Criminal', 5), ('Entertainer', 5), ('Folk Hero', 10),
                    ('Guild Artisan', 0), ('Hermit', 5), ('Noble', 20),
                    ('Outlander', 10), ('Sage', 15), ('Sailor', 5),
                    ('Soldier', 20), ('Urchin', 5)),
        "Warlock": (('Acolyte', 5), ('Charlatan', 5),
                    ('Criminal', 5), ('Entertainer', 5), ('Folk Hero', 10),
                    ('Guild Artisan', 15), ('Hermit', 5), ('Noble', 10),
                    ('Outlander', 10), ('Sage', 25), ('Sailor', 10),
                    ('Soldier', 5), ('Urchin', 10)),
        "Wizard": (('Acolyte', 10), ('Charlatan', 5),
                   ('Criminal', 10), ('Entertainer', 5), ('Folk Hero', 10),
                   ('Guild Artisan', 15), ('Hermit', 5), ('Noble', 10),
                   ('Outlander', 10), ('Sage', 25), ('Sailor', 10),
                   ('Soldier', 5), ('Urchin', 5)),
        "Barbarian": (('Acolyte', 5), ('Charlatan', 5),
                      ('Criminal', 15), ('Entertainer', 10), ('Folk Hero', 10),
                      ('Guild Artisan', 10), ('Hermit', 5), ('Noble', 5),
                      ('Outlander', 20), ('Sage', 5), ('Sailor', 10),
                      ('Soldier', 5), ('Urchin', 10)),
        "Fighter": (('Acolyte', 10), ('Charlatan', 15),
                    ('Criminal', 15), ('Entertainer', 15), ('Folk Hero', 20),
                    ('Guild Artisan', 10), ('Hermit', 5), ('Noble', 20),
                    ('Outlander', 15), ('Sage', 10), ('Sailor', 15),
                    ('Soldier', 25), ('Urchin', 15)),
        "Rouge": (('Acolyte', 5), ('Charlatan', 25),
                  ('Criminal', 20), ('Entertainer', 15), ('Folk Hero', 10),
                  ('Guild Artisan', 5), ('Hermit', 5), ('Noble', 10),
                  ('Outlander', 15), ('Sage', 10), ('Sailor', 15),
                  ('Soldier', 5), ('Urchin', 20)),
        "Monk": (('Acolyte', 30), ('Charlatan', 5),
                 ('Criminal', 5), ('Entertainer', 5), ('Folk Hero', 5),
                 ('Guild Artisan', 15), ('Hermit', 5), ('Noble', 15),
                 ('Outlander', 15), ('Sage', 20), ('Sailor', 5),
                 ('Soldier', 5), ('Urchin', 5)),
        "Bard": (('Acolyte', 10), ('Charlatan', 25),
                 ('Criminal', 15), ('Entertainer', 30), ('Folk Hero', 10),
                 ('Guild Artisan', 15), ('Hermit', 5), ('Noble', 10),
                 ('Outlander', 5), ('Sage', 10), ('Sailor', 15),
                 ('Soldier', 5), ('Urchin', 15)),
        "Sorcerer": (('Acolyte', 10), ('Charlatan', 15),
                     ('Criminal', 5), ('Entertainer', 5), ('Folk Hero', 10),
                     ('Guild Artisan', 10), ('Hermit', 5), ('Noble', 15),
                     ('Outlander', 10), ('Sage', 20), ('Sailor', 10),
                     ('Soldier', 5), ('Urchin', 10))
    }

    try:
        background = weighted_choice(d[pc_class])
        bg_data = get_background_list('data/char/' + background.lower() + 'Background')
        traits = random.sample(bg_data[0], 2)
        trait = traits[0] + " " + traits[1]
        ideal = random.choice(bg_data[1])
        bond = random.choice(bg_data[2])
        flaw = random.choice(bg_data[3])
        specialty = random.choice(bg_data[4])
        feature = random.choice(bg_data[5])

        return trait, ideal, bond, flaw, specialty, background, feature
    except Exception as err:
        print err
        return 'FAIL', 'FAIL', 'FAIL', 'FAIL', 'FAIL', 'FAIL', 'FAIL'


def get_proficiencies(pc_race, pc_subrace):
    global pc

    bg_d = {
        'Acolyte': ('SK Insight', 'SK Religion', '+2 Languages'),
        'Charlatan': ('SK Deception', 'SK Slight of Hand',
                      'Disguise Kit', 'Forgery Kit'),
        'Criminal': ('SK Deception', 'SK Stealth',
                     'Gaming Set', 'Thieves Tools'),
        'Entertainer': ('SK Acrobatics', 'SK Performance',
                        'Disgise Kit', 'Musical Instrument'),
        'Folk Hero': ('SK Animal Handling', 'SK Survival',
                      "Artisan's tools", 'Land vehicles'),
        'Guild Artisan': ('SK Insight', 'SK Persuasion',
                          "Artisan's tools", '+1 Language'),
        'Hermit': ('SK Medicine', 'SK Religion',
                   'Herbalism Kit', '+1 Language'),
        'Noble': ('SK History', 'SK Persuasion',
                  'Gaming Set', '+1 Language'),
        'Outlander': ('SK Athletics', 'SK Survival',
                      'Musical Instrument', '+1 Language'),
        'Sage': ('SK Arcana', 'SK History',
                 '+2 Language'),
        'Sailor': ('SK Athletics', 'SK Perception',
                   "Navigator's Tools", 'Water vehicles'),
        'Soldier': ('SK Athletics', 'SK Intimidation',
                    'Gaming set', 'Land vehicles'),
        'Urchin': ('SK Slight of Hand', 'SK Stealth',
                   'Disguise Kit', "Thieves' tools"),
    }

    for k, v in bg_d.iteritems():
        if pc['Background'] == k:
            for prof in v:
                pc['Prof'].append(prof)

    if pc['Race'] == "Dwarf":
        pc['Prof'].append('Battleaxe')
        pc['Prof'].append('Handaxe')
        pc['Prof'].append('Throwing Hammer')
        pc['Prof'].append('Warhammer')
        pc['Prof'].append(random.choice(("Smith’s tools", "Brewer’s supplies", "Mason’s tools")))
    if pc['Subrace'] == 'Mountain':
        pc['Prof'].append('Light Armor')
        pc['Prof'].append('Medium Armor')
    if (pc['Subrace'] == 'High') or (pc['Subrace'] == 'Wood'):
        pc['Prof'].append('Longsword')
        pc['Prof'].append('Shortsword')
        pc['Prof'].append('Shortbow')
        pc['Prof'].append('Longbow')
    if pc['Subrace'] == 'Dark':
        pc['Prof'].append('Rapier')
        pc['Prof'].append('Shortsword')
        pc['Prof'].append('Hand Crossbow')

    pro_d = {
        "Fighter": ('Heavy armor', 'Light armor', 'Medium armor', 'Shields',
                    'Simple weapons', 'Martial weapons', 'ST Strength',
                    'ST Constitution'),
        "Ranger": ('Light armor', 'Medium armor', 'Shields',
                   'Simple weapons', 'Martial weapons', 'ST Strength ',
                   'ST Dexterity '),
        "Barbarian": ('Light armor', 'Medium armor', 'Shields',
                      'Simple weapons', 'Martial weapons', 'ST Strength',
                      'ST Constitution '),
        "Wizard": ('Daggers', 'Darts', 'Slings', 'Quarterstaffs',
                   'Light crossbows', 'ST Intelligence', 'ST Wisdom'),
        "Cleric": ('Light armor', 'Medium armor', 'Shields',
                   'Simple weapons', 'ST Wisdom', 'ST Charisma'),
        "Bard": ('Light armor', 'Simple weapons', 'Hand crossbows',
                 'Longswords', 'Rapiers', 'Shortswords', 'ST Dexterity',
                 'ST Charisma'),
        "Druid": ('Light armor (nonmetal)', 'Medium armor (nonmetal)',
                  'Shields (nonmetal)', 'Clubs', 'Daggers',
                  'Darts', 'javelins', 'Maces', 'Quarterstaffs',
                  'Scimitars', 'Sickles', 'Slings', 'Spears',
                  'ST Intelligence', 'ST Wisdom'),
        "Monk": ('Simple weapons', 'Shortswords', 'ST Strength',
                 'ST Dexterity'),
        "Paladin": ('Heavy armor', 'Light armor', 'Medium armor', 'Shields',
                    'Simple weapons', 'Martial weapons', 'ST Wisdom',
                    'ST Charisma'),
        "Rouge": ('Light armor', 'Simple weapons', 'Hand crossbows',
                  'Longswords', 'Rapiers', 'Shortswords', 'ST Dexterity',
                  'ST Intelligence'),
        "Sorcerer": ('Daggers', 'Darts', 'Slings', 'Quarterstaffs',
                     'Light crossbows', 'ST Constitution', 'ST Charisma'),
        "Warlock": ('Light armor', 'Simple weapons', 'ST Wisdom',
                    'ST Charisma'),
    }
    for k, v in pro_d.iteritems():
        if pc['Class'] == k:
            for prof in v:
                pc['Prof'].append(prof)


def get_languages(pc_race):
    try:
        pc_langlist = ("Elvish", "Dwarvish", "Orcish", "Halfling")
        if pc_race == "Human":
            pc_lang = ("Common", random.choice(pc_langlist))
        elif pc_race == "Dwarf":
            pc_lang = ("Common", "Dwarvish")
        elif (pc_race == "Elf") or (pc_race == 'Half-Elf'):
            pc_lang = ("Common", "Elvish")
        elif pc_race == "Halfling":
            pc_lang = ("Common", "Halfling")
        elif pc_race == "Dragonborn":
            pc_lang = ("Common", "Draconic")
        elif pc_race == "Gnome":
            pc_lang = ("Common", "Gnomish")
        elif pc_race == "Half-Orc":
            pc_lang = ("Common", "Orc")
        elif pc_race == "Tiefling":
            pc_lang = ("Common", "Infernal")
        else:
            pc_lang = ("Error", "No Languages for race defined")
        return pc_lang
    except:
        print 'ERROR IN GET_LANGUAGES'
        return 'Error'


def get_age(pc_race):
    try:
        if pc_race == "Human":
            return random.randint(14, 50)
        elif pc_race == "Elf":
            return random.randint(25, 500)
        elif pc_race == "Dwarf":
            return random.randint(50, 270)
        elif pc_race == "Halfling":
            return random.randint(20, 110)
        elif pc_race == "Dragonborn":
            return random.randint(15, 80)
        elif pc_race == "Gnome":
            return random.randint(40, 400)
        elif pc_race == "Half-Elf":
            return random.randint(20, 160)
        elif pc_race == "Half-Orc":
            return random.randint(14, 65)
        elif pc_race == "Tiefling":
            return random.randint(14, 60)
    except:
        print "ERROR IN GET_AGE"
        return 1


def get_speed(pc_race, pc_subrace):
    if (pc_race == "Dwarf") or (pc_race == 'Gnome'):
        return 25
    elif pc_subrace == "Wood":
        return 35
    else:
        return 30


def get_height_weight(pc_race, pc_subrace):
    """
    Filled with h/w of corresponding races as of DND5e player guide
    """
    try:
        if (pc_race == 'Human') or (pc_race == 'Half-Elf') or (pc_race == 'Tiefling'):
            h = (140 + random.randint(5, 50))
            w = (50 * (1 + random.random()) * 1.2)
        elif (pc_race == "Halfling") or (pc_race == 'Gnome'):
            h = (78 + random.randint(5, 20))
            w = (22 * (1 + random.random()))
        elif pc_subrace == "Wood":
            h = (130 + random.randint(5, 50))
            w = (45 * (1 + random.random()) * 1.2)
        elif pc_subrace == "Dark":
            h = (125 + random.randint(5, 30))
            w = (32 * (1 + random.random()) * 2.2)
        elif pc_subrace == "High":
            h = (130 + random.randint(5, 50))
            w = (48 * (1 + random.random()) * 1.2)
        elif pc_subrace == "Hill":
            h = (120 + random.randint(5, 20))
            w = (52 * (1 + random.random()) * 2.2)
        elif pc_subrace == "Mountain":
            h = (140 + random.randint(5, 20))
            w = (60 * (1 + random.random()) * 2.2)
        elif pc_race == "Dragonborn":
            h = (170 + random.randint(5, 40))
            w = (92 * (1 + random.random()) * 2.2)
        elif pc_race == "Half-Orc":
            h = (155 + random.randint(5, 20))
            w = (65 * (1 + random.random()) * 2.2)
        return int(h), int(w)
    except:
        print "ERROR IN GETH/W"
        return 0, 0


def settings_config(pc_config):
    global new_class, newRace, pcLevel
    if pc_config['use']:
        pcLevel = pc_config['Level']#random.randint(1, pc_config['Level']+ random.randint(0,3))
        newRace = pc_config['Race']
        new_class = pc_config['Class']
    else:
        pcLevel = random.randint(1, 4)
        new_class = None
        newRace = None


def main():
    """
    Used to output character's dictionary.
    :rtype : pc_dict
    """
    global pc

    pc = {'Prof': list(), 'Traits': list(), 'Level': pcLevel}
    pc['prof_level'] = get_prof_level(pc['Level'])

    pc['Class'] = get_stats()

    if new_class is not None:
        if new_class.title() in classesTup:
            pc['Class'] = force_class(pc['Class'])
    pc['Gender'] = random.choice(('Male', 'Female'))
    pc['Race'] = get_race(pc['Class'])
    if newRace is not None:
        if newRace.title() in racesTup:
            pc['Race'] = newRace.title()
    pc['Subrace'] = get_race_bonus(pc['Race'])

    pc['strMod'] = get_stat_modifiers(pc['STR'])
    pc['dexMod'] = get_stat_modifiers(pc['DEX'])
    pc['conMod'] = get_stat_modifiers(pc['CON'])
    pc['intMod'] = get_stat_modifiers(pc['INT'])
    pc['wisMod'] = get_stat_modifiers(pc['WIS'])
    pc['chrMod'] = get_stat_modifiers(pc['CHR'])

    pc['Alignment'] = get_alignment(pc['Race'])
    pc['Name'] = get_name(pc['Race'], pc['Gender'])
    pc['Speed'] = get_speed(pc['Race'], pc['Subrace'])
    pc['Age'] = get_age(pc['Race'])
    pc['Lang'] = get_languages(pc['Race'])
    pc['Height'], pc['Weight'] = get_height_weight(pc['Race'], pc['Subrace'])

    (pc['Trait'], pc['Idea'], pc['Bond'], pc['Flaw'],
     pc['Specialty'], pc['Background'], pc['Feature']) = get_background(pc['Class'])
    get_proficiencies(pc['Race'], pc['Subrace'])

    bio = """
BIO:
	Name:	%s
	Gender:	%s
	Race:   %s %s
	Class:	%s
	Background:	%s
	Age:	%s	Height:	%dcm
	Align:	%s	Weight:	%dkg
	Lang:	%s

	"""%(pc['Name'], pc['Gender'], pc['Race'], pc['Subrace'],
               pc['Class'], pc['Background'], pc['Age'],
               pc['Height'], pc['Alignment'],pc['Weight'],
               ", ".join([str(x) for x in pc['Lang']]))  # to get rid of ugly formatting

    pc['HP'] = get_hitpoints(pc['Class'], pc['Level'], pc['Subrace'])
    pc['Speed'] = get_speed(pc['Race'], pc['Subrace'])

    stats = """
STATS:
	Level:	%d
	HP:	%d
	Speed:	%d

	STR	%d (%d)
	DEX	%d (%d)
	CON	%d (%d)
	INT	%d (%d)
	WIS	%d (%d)
	CHR	%d (%d)

"""%(pc['Level'], pc['HP'], pc['Speed'], pc['STR'], pc['strMod'], pc['DEX'], pc['dexMod'], pc['CON'],
           pc['conMod'], pc['INT'], pc['intMod'], pc['WIS'], pc['wisMod'], pc['CHR'], pc['chrMod'])

    pc['Spells'] = get_spells(pc['Class'], pc['Level'])

    def neat_list_return(li):
        s = str()
        for item in li:
            if item != 'None':
                s += item + '\n'
            else:
                return 'None\n'
        return s

    spells = str()
    if pc['Spells']:
        spells += "\nCANTRIPS:\n" + neat_list_return(pc['Spells'][0])
        c = 1
        for spell in xrange(0, pc['Level']):
            try:
                spells += "\nLEVEL %d:\n"%c+(neat_list_return(pc['Spells'][c]))
                c += 1
            except:
                break
    else:
        spells = "\nNo Spells\n"

    item_d = itemGen.main('wep', 'rnd')
    weapon = '''
WEAPON:
	Name: 	 %s
	Range:	 %s
	Hit Die: %s
	Dam Type:%s

	'''%(item_d['Name'], item_d['Weapon Type'],
               item_d['Hit Die'], item_d['Damage Type'])

    armor_d = itemGen.main('arm', 'rnd')
    armor = '''
ARMOR:
	Name:	%s
	Type:	%s
	AC:	    %s
	Cost:	%s
	'''%(armor_d['Name'], armor_d['Type'],
               armor_d['AC'], armor_d['Cost'])

    proficiencies = 'PROFICIENCIES:\n'
    for prof in pc['Prof']:
        proficiencies += "\t%s\n" % prof

    traits = 'TRAITS:\n'
    for trait in pc['Traits']:
        traits += "\t%s\n" % trait

    background = '''
BACKGROUND:
TRAITS:\n%s

IDEAL:\n%s

BOND:\n%s

FLAW:\n%s

SPECIALTY:\n%s

FEATURE:\n%s
	'''%(pc['Trait'], pc['Idea'],
               pc['Bond'], pc['Flaw'], pc['Specialty'], pc['Feature'])

    try:
        pc['Info'] = bio + stats + proficiencies + traits + weapon + armor + spells + background
    except Exception as err:
        print err

    return pc


def custom_param(pc_config):
    settings_config(pc_config['char'])
    sheet = main()
    return sheet


if __name__ == '__main__':
    import def_settings

    default_settings = def_settings.get_def_settings()
    settings_config(default_settings['char'])
    main()
    print pc['Info']
