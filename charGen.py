#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  charGen.py
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
#  Responsible for generation of characters, their stats, abilites,
#  and bios. Passes to townGen to populate buildings with people

try:
	import random
	import argparse
	import itemGen
except ImportError:
	print "You are missing essential Libraries. See README.md"


racesTup = 	('Human','Elf','Dwarf','Halfling','Half-Elf','Half-Orc',
			'Dragonborn','Gnome')
classesTup = ('Cleric','Druid','Ranger','Paladin','Warlock','Wizard',
			'Barbarian','Fighter','Rouge','Monk','Bard','Sorcerer',
			'Commoner')

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
def getFromFile_LoL(fi):
	fi = open(fi)
	# Builds a list of lists from a file, seperated by newline
	li = [i.strip().split(',') for i in fi.readlines() if not i.startswith("#")]
	# ignore blank lines
	li = [x for x in li if x != ['']]
	li = [[st.strip() for st in l] for l in li]
	fi.close()
	return li
def getFromFile_Dic(fi):
	d = {}
	with open(fi) as f:
		for line in f:
			if not line.startswith("#"):
				(key, val) = line.strip().split('=')
				d[key] = val
	return d

def get_background_list(fi):
	fi = open(fi)
	# Builds a list of lists from a file, seperated by newline
	li = [i.strip().split('::') for i in fi.readlines() if not i.startswith("#")]
	# ignore blank lines
	li = [x for x in li if x != ['']]
	li = [[st.strip() for st in l] for l in li]
	fi.close()
	return li

def forceClass(pcClass):
	'''
	Innefficent way of forcing a class, but since the stats are random,
	and need to go along with what sort of class you get, this is the way
	to do it.
	'''
	global newClass
	lowClass = pcClass.lower()
	lowNew = newClass.lower()
	while lowClass != lowNew:
		pcClass = getStats()
		lowClass = pcClass.lower()
	return pcClass


def getStats():
	'''
	Gets both stats and class, should probably be broken up into seperate
	functions, but works fine, really. Could be moved to main(), but that
	would just make main() more bloated, no need.
	'''
	global pc
	if newClass == 'Commoner':
		pc['STR'] = pc['DEX'] = pc['CON'] = 10
		pc['INT'] = pc['WIS'] = pc['CHR'] = 10
		return 'Commoner'
	pc['STR'] = getStatRoll();pc['DEX'] = getStatRoll();pc['CON'] = getStatRoll()
	pc['INT'] = getStatRoll();pc['WIS'] = getStatRoll();pc['CHR'] = getStatRoll()
	statTup = (pc['STR'], pc['DEX'], pc['CON'], pc['INT'], pc['WIS'], pc['CHR'])

	try:
		if statTup[0] == max(statTup):
			tup = (('Barbarian',5),('Fighter',3),('Paladin',3))
		elif statTup[1] == max(statTup):
			tup = (('Rouge',5),('Ranger',3),('Monk',3),('Fighter',3))
		elif statTup[2] == max(statTup):
			tup = (('Barbarian',5),('Fighter',3),('Sorcerer',1))
		elif statTup[3] == max(statTup):
			tup = (('Wizard',5),('Rouge',1),('Druid',1))
		elif statTup[4] == max(statTup):
			tup = (('Cleric',5),('Druid',5),('Ranger',3),
				('Paladin',1),('Warlock',1),('Wizard',1))
		elif statTup[5] == max(statTup):
			tup = (('Bard',5),('Sorcerer',5),('Warlock',5),
				('Paladin',3),('Cleric',1))
		return wChoice(tup)
	except:
		print "GETSTATS ERROR: DEFAULTING TO FIGHTER"
		return 'Fighter'

def getStatModifiers(st):
    return st / 2  - 5

def getStatRoll():
	'''
	Meant to accurately emulate a 4d6d1
	'''
	r1 = random.randint(1,6)
	r2 = random.randint(1,6)
	r3 = random.randint(1,6)
	r4 = random.randint(1,6)
	rList = [r1,r2,r3,r4]
	rList.pop(mini(rList))
	return (rList[0] + rList[1] + rList[2])

def getRaceBonus(pcRace):
	'''
	Easy, but ugly way to get bonuses per race, but since we have
	to use strings to compare things, this is the only way to go.
	Also, it may be better to make subrace in a different function, or even
	in getRace() itself, since this is messy.
	'''
	global pc
	if pcRace == "Dwarf":
		subraces 	= ('Mountain','Hill')
		pc['CON'] +=2
	elif pcRace == "Elf":
		subraces	= ('High','Wood','Dark')
		pc['DEX'] += 2
	elif pcRace == "Halfling":
		subraces= ('Lightfoot','Stout')
		pc['DEX'] += 2
	elif pcRace == "Human":
		subraces = ('Calishite','Chondathan','Shou','Damaran',
		'Tethyrian','Illuskan','Turami','Mulan','Rashemi')
		pc['STR'] += 1; pc['DEX'] += 1; pc['CON'] +=1
		pc['INT'] +=1; pc['WIS'] +=1; pc['CHR'] += 1
	elif pcRace == "Dragonborn":
		subraces = ('Black','Blue','Brass','Bronze','Copper',
		'Gold','Green','Red','White','Silver')
		pc['STR'] +=2; pc['CHR'] +=1
	elif pcRace == "Gnome":
		subraces = ('Forest','Rock')
		pc['DEX'] +=1
	elif pcRace == 'Half-Elf':
		pc['CHR'] +=2
	elif pcRace == 'Half-Orc':
		pc['STR'] +=2; pc['CON'] +=1
	elif pcRace == 'Tiefling':
		pc['INT'] +=1; pc['CHR'] +=2
	try:
		pcSubrace = random.choice(subraces)
		getSubraceBonus(pcSubrace)
	except:
		pcSubrace = ""
	return pcSubrace

def getSubraceBonus(pcSubrace):
	global pc
	if pcSubrace == 'Hill':
			pc['WIS'] += 1
	elif pcSubrace == "Mountain":
			pc['STR'] += 2
	elif pcSubrace == "High":
			pc['INT'] += 1
	elif pcSubrace == "Wood":
			pc['WIS'] += 1
	elif pcSubrace == "Dark":
			pc['CHR'] += 1
	elif pcSubrace == 'Lightfoot':
			pc['CHR'] += 1
	elif pcSubrace == 'Stout':
			pc['CON'] += 1
	elif pcSubrace == 'Forest':
			pc['DEX'] += 1
	elif pcSubrace == 'Rock':
			pc['CON'] += 1

def getHitPoints(pcClass, conMod, pcLevel, pcSubrace):
	'''
	It's best to use a dictionary here, to avoid messy shit like
	what exists above. Unfortunately, that wouldn't work up there because
	of the varying data that gets changed. This cannot be any more efficent.
	'''
	hpBonus = 0
	try:
		hit_dies = {
		'Sorcerer': 6, 'Wizard':6, 'Bard':8,
		'Fighter': 10, 'Paladin':10, 'Ranger': 10,
		'Barbarian': 12, 'Cleric': 8, 'Druid': 8,
		'Monk':8, 'Rouge':8, 'Warlock':8
		}


		if pcSubrace == 'Hill':
			hpBonus = 1

		if pcClass == 'Commoner':
			 hit_points = random.randint(1,8)
		else:
			hit_points = hit_dies[pcClass] + pc['conMod'] + hpBonus

		if pcLevel == 1:
			return hit_points

		for x in xrange(1,pcLevel):
			hit_points = hit_points + random.randint(1,hit_dies[pcClass]) + pc['conMod'] + hpBonus
		return hit_points
	except:
		return 1

def getRace(pcClass):
	'''
	Very autistic way of representing slightly different tendancies based
	upon one variable, but I'm unaware of any other mathematical expression
	or method that would make this easier.
	'''
	try:
		if pcClass == "Fighter":
			raceList = 	(('Dwarf',10),('Elf',5),('Halfling',5),('Human',25),
			('Dragonborn',3),('Gnome',2),('Half-Elf',5),('Half-Orc',5),('Tiefling',2))
		elif pcClass == "Ranger":
			raceList = 	(('Dwarf',10),('Elf',15),('Halfling',5),('Human',25),
			('Dragonborn',1),('Gnome',5),('Half-Elf',5),('Half-Orc',1),('Tiefling',1))
		elif pcClass == "Barbarian":
			raceList = 	(('Dwarf',15),('Elf',5),('Halfling',5),('Human',25),
			('Dragonborn',3),('Gnome',1),('Half-Elf',2),('Half-Orc',10),('Tiefling',3))
		elif pcClass == "Wizard":
			raceList = 	(('Dwarf',5),('Elf',15),('Halfling',5),('Human',25),
			('Dragonborn',2),('Gnome',8),('Half-Elf',10),('Half-Orc',1),('Tiefling',2))
		elif pcClass == "Cleric":
			raceList = 	(('Dwarf',5),('Elf',15),('Halfling',5),('Human',25),
			('Dragonborn',2),('Gnome',2),('Half-Elf',10),('Half-Orc',2),('Tiefling',2))
		elif pcClass == "Bard":
			raceList = 	(('Dwarf',5),('Elf',15),('Halfling',15),('Human',25),
			('Dragonborn',5),('Gnome',5),('Half-Elf',10),('Half-Orc',5),('Tiefling',5))
		elif pcClass == "Druid":
			raceList = 	(('Dwarf',5),('Elf',15),('Halfling',5),('Human',25),
			('Dragonborn',2),('Gnome',2),('Half-Elf',7),('Half-Orc',5),('Tiefling',2))
		elif pcClass == "Monk":
			raceList = 	(('Dwarf',10),('Elf',10),('Halfling',5),('Human',25),
			('Dragonborn',3),('Gnome',2),('Half-Elf',6),('Half-Orc',5),('Tiefling',4))
		elif pcClass == "Paladin":
			raceList = 	(('Dwarf',15),('Elf',5),('Halfling',5),('Human',25),
			('Dragonborn',5),('Gnome',2),('Half-Elf',7),('Half-Orc',10),('Tiefling',2))
		elif pcClass == "Rouge":
			raceList = 	(('Dwarf',8),('Elf',20),('Halfling',10),('Human',25),
			('Dragonborn',2),('Gnome',8),('Half-Elf',5),('Half-Orc',1),('Tiefling',2))
		elif pcClass == "Sorcerer":
			raceList = 	(('Dwarf',10),('Elf',10),('Halfling',10),('Human',25),
			('Dragonborn',2),('Gnome',4),('Half-Elf',11),('Half-Orc',1),('Tiefling',2))
		elif pcClass == "Warlock":
			raceList = 	(('Dwarf',10),('Elf',10),('Halfling',10),('Human',25),
			('Dragonborn',2),('Gnome',4),('Half-Elf',11),('Half-Orc',1),('Tiefling',2))
		elif pcClass == 'Commoner':
			raceList = (('Dwarf',15),('Elf',15),('Halfling',15),('Human',50),
			('Dragonborn',5),('Gnome',5),('Half-Elf',10),('Half-Orc',5),('Tiefling',5))
		return wChoice(raceList)
	except:
		print "ERROR in getRace"
		return 'Human'


def getAlignment(pcRace):
	try:
		if pcRace == "Human" :
			alignmentList= (('N' ,1),('CG' ,1),('CN' ,1),('CE',1),
			('LG' ,1),('LN' ,1),('LE' ,1),('NE',1),('NG',1))
		elif pcRace == "Dwarf" :
			alignmentList= (('N' ,20),('CG' ,10),('CN' ,50),('CE',5),
			('LG',15),('LN',10),('LE' ,5),('NE',5),('NG',5))
		elif pcRace == "Halfling" :
			alignmentList= (('N' ,2),('CG' ,2),('CN' ,2),('CE',1),
			('LG',20),('LN',2),('LE' ,2),('NE',2),('NG',2))
		elif pcRace == "Elf" :
			alignmentList= (('N' ,10),('CG' ,20),('CN' ,10),('CE',5),
			('LG',15),('LN',30),('LE' ,5),('NE',5),('NG',5))
		elif pcRace == "Dragonborn":
			alignmentList= (('N' ,1),('CG' ,2),('CN' ,1),('CE',8),
			('LG' ,35),('LN' ,1),('LE' ,1),('NE',2),('NG',2))
		elif pcRace == "Gnome":
			alignmentList= (('N' ,15),('CG' ,20),('CN' ,2),('CE',1),
			('LG' ,20),('LN' ,2),('LE' ,1),('NE',1),('NG',5))
		elif pcRace == "Half-Elf":
			alignmentList= (('N' ,15),('CG' ,25),('CN' ,20),('CE',5),
			('LG' ,25),('LN' ,20),('LE' ,7),('NE',5),('NG',15))
		elif pcRace == "Half-Orc":
			alignmentList= (('N' ,10),('CG' ,15),('CN' ,5),('CE',20),
			('LG' ,5),('LN' ,10),('LE' ,20),('NE',15),('NG',10))
		elif pcRace == "Tiefling":
			alignmentList= (('N' ,8),('CG' ,15),('CN' ,15),('CE',15),
			('LG' ,10),('LN' ,8),('LE' ,12),('NE',5),('NG',5))

		return wChoice(alignmentList)
	except:
		return "Error in Alignment"


def getName(pcRace, pcGender):
	'''
	This is a nice snippet. It looks for a filename corresponding with the
	race name in a paticular syntax, then imports all sorts of different names
	based opon their index in a list of lists.
	'''
	global pc
	try:
		names = getFromFile_LoL('data/char/'+(pcRace.lower()+'Names'))
		pc['Last Name'] = random.choice(names[2])
		if pcGender == 'Male':
			pc['First Name'] = random.choice(names[0])
		else:
			pc['First Name'] = random.choice(names[1])
		# if we want special exceptions
		#if pcNameFirst == "Helga": pcNameLast = "SMASH";pc['STR'] += 10
		pcName = pc['First Name'] + ' '+  pc['Last Name']
	except:
		pcName = "Error- No cfg file for %s" %pcRace
	return pcName


def getSpells(pcClass, pcLevel):
	'''
	Similar in build to getName(), however it uses a dict to find out
	how many spell slots a character can/will use, dependant on their level,
	and then returns a predetermined number of random spells as designated in
	their class spell file.
	However cool this is, it is not accurate with the DNDv5 book, for building
	a character that a player would use, it would need to simply return a set of
	known spells, based on level, and then list the amount of spell slots they would
	have. That is much simpler, but since this is meant for npcs, it doens't matter.
	'''
	if pcLevel > 20:
		pcLevel = 20
	#'class':(cantrips,total spells,lvl1,lvl2,etc...)
	stdSlots = {
	1:(2,2),				2:(2,3),
	3:(2,4,2),				4:(3,4,3),
	5:(3,4,3,2),			6:(3,4,3,3),
	7:(3,4,3,3,1),			8:(3,4,3,3,2),
	9:(3,4,3,3,3,1),		10:(4,4,3,3,3,2),
	11:(4,4,3,3,3,2,1),		12:(4,4,3,3,3,2,1),
	13:(4,4,3,3,3,2,1,1),	14:(4,4,3,3,3,2,1,1),
	15:(4,4,3,3,3,2,1,1,1),	16:(4,4,3,3,3,2,1,1,1),
	17:(4,4,3,3,3,2,1,1,1,1),18:(4,4,3,3,3,3,1,1,1,1),
	19:(4,4,3,3,3,3,2,1,1,1),20:(4,4,3,3,3,3,2,2,1,1),
	}
	curSlots = stdSlots[pcLevel]
	try:
		spells = list()
		spellLoL = getFromFile_LoL('data/char/'+(pcClass.lower()+'Spells'))
		for spell in spellLoL:
			random.shuffle(spell)
		for s, l in zip(spellLoL, curSlots):
			spells.append(s[0:l])
		return spells
	except:
		return None

def getSkills(pcRace, pcClass):
	skills = dict()
	if pcRace == "Dwarf":
		pass

def getBackground(pcClass):
	if pcClass == "Cleric":
		charBackground = (('Acolyte', 25), ('Charlatan', 5),
			('Criminal', 5), ('Entertainer', 5), ('Folk Hero', 10),
			('Guild Artisan', 5), ('Hermit', 5), ('Noble', 10),
			('Outlander', 5), ('Sage', 15), ('Sailor', 5),
			('Soldier', 5), ('Urchin', 5))
	elif pcClass == "Druid":
		charBackground = (('Acolyte', 20), ('Charlatan', 5),
			('Criminal', 5), ('Entertainer', 5), ('Folk Hero', 10),
			('Guild Artisan', 5), ('Hermit', 5), ('Noble', 10),
			('Outlander', 10), ('Sage', 20), ('Sailor', 5),
			('Soldier', 5), ('Urchin', 10))
	elif pcClass == "Ranger":
		charBackground = (('Acolyte', 15), ('Charlatan', 15),
			('Criminal', 10), ('Entertainer', 10), ('Folk Hero', 15),
			('Guild Artisan', 10), ('Hermit', 5), ('Noble', 15),
			('Outlander', 10), ('Sage', 15), ('Sailor', 5),
			('Soldier', 15), ('Urchin', 10))
	elif pcClass == "Paladin":
		charBackground =  (('Acolyte', 20), ('Charlatan', 10),
			('Criminal', 5), ('Entertainer', 5), ('Folk Hero', 10),
			('Guild Artisan', 0), ('Hermit', 5), ('Noble', 20),
			('Outlander', 10), ('Sage', 15), ('Sailor', 5),
			('Soldier', 20), ('Urchin', 5))
	elif pcClass == "Warlock":
		charBackground = (('Acolyte', 5), ('Charlatan', 5),
			('Criminal', 5), ('Entertainer', 5), ('Folk Hero', 10),
			('Guild Artisan', 15), ('Hermit', 5), ('Noble', 10),
			('Outlander', 10), ('Sage', 25), ('Sailor', 10),
			('Soldier', 5), ('Urchin', 10))
	elif pcClass == "Wizard":
		charBackground = (('Acolyte', 10), ('Charlatan', 5),
			('Criminal', 10), ('Entertainer', 5), ('Folk Hero', 10),
			('Guild Artisan', 15), ('Hermit', 5), ('Noble', 10),
			('Outlander', 10), ('Sage', 25), ('Sailor', 10),
			('Soldier', 5), ('Urchin', 5))
	elif pcClass == "Barbarian":
		charBackground = (('Acolyte', 5), ('Charlatan', 5),
			('Criminal', 15), ('Entertainer', 10), ('Folk Hero', 10),
			('Guild Artisan', 10), ('Hermit', 5), ('Noble', 5),
			('Outlander', 20), ('Sage', 5), ('Sailor', 10),
			('Soldier', 5), ('Urchin', 10))
	elif pcClass == "Fighter":
		charBackground = (('Acolyte', 10), ('Charlatan', 15),
			('Criminal', 15), ('Entertainer',15), ('Folk Hero', 20),
			('Guild Artisan', 10), ('Hermit', 5), ('Noble', 20),
			('Outlander', 15), ('Sage', 10), ('Sailor', 15),
			('Soldier', 25), ('Urchin', 15))
	elif pcClass == "Rouge":
		charBackground = (('Acolyte', 5), ('Charlatan', 25),
			('Criminal', 20), ('Entertainer', 15), ('Folk Hero', 10),
			('Guild Artisan', 5), ('Hermit', 5), ('Noble', 10),
			('Outlander', 15), ('Sage', 10), ('Sailor', 15),
			('Soldier', 5), ('Urchin', 20))
	elif pcClass == "Monk":
		charBackground = (('Acolyte', 30), ('Charlatan', 5),
			('Criminal', 5), ('Entertainer', 5), ('Folk Hero', 5),
			('Guild Artisan', 15), ('Hermit', 5), ('Noble', 15),
			('Outlander', 15), ('Sage', 20), ('Sailor', 5),
			('Soldier', 5), ('Urchin', 5))
	elif pcClass == "Bard":
		charBackground = (('Acolyte', 10), ('Charlatan', 25),
			('Criminal', 15), ('Entertainer', 30), ('Folk Hero', 10),
			('Guild Artisan', 15), ('Hermit', 5), ('Noble', 10),
			('Outlander', 5), ('Sage', 10), ('Sailor', 15),
			('Soldier', 5), ('Urchin', 15))
	elif pcClass == "Sorcerer":
		charBackground = (('Acolyte', 10), ('Charlatan', 15),
			('Criminal', 5), ('Entertainer', 5), ('Folk Hero', 10),
			('Guild Artisan', 10), ('Hermit', 5), ('Noble', 15),
			('Outlander', 10), ('Sage', 20), ('Sailor', 10),
			('Soldier', 5), ('Urchin', 10))
	elif pcClass == 'Commoner':
		charBackground = (('Acolyte', 3), ('Charlatan', 3),
			('Criminal', 15), ('Entertainer', 15), ('Folk Hero', 3),
			('Guild Artisan', 15), ('Hermit', 15), ('Noble', 15),
			('Outlander', 5), ('Sage', 3), ('Sailor', 10),
			('Soldier', 3), ('Urchin', 3))

	try:
		background = wChoice(charBackground)
		bgData = get_background_list('data/char/'+background.lower()+'Background')
		traits = random.sample(bgData[0],2)
		trait = traits[0] + " " + traits[1]
		ideal = random.choice(bgData[1])
		bond = random.choice(bgData[2])
		flaw = random.choice(bgData[3])
		specialty = random.choice(bgData[4])
		feature = random.choice(bgData[5])

		return trait, ideal, bond, flaw, specialty, background, feature
	except Exception as err:
		print err
		return 'FAIL','FAIL','FAIL','FAIL','FAIL', 'FAIL', 'FAIL'


def getProficiencies(pcRace, pcSubrace):
	plist = list()
	if pcRace == "Dwarf":
		plist.append['Battleaxe','Handaxe','Throwing Hammer',
		'Warhammer', 'Light Armor', 'Medium Armor']
	if (pcSubrace == 'High') or (pcSubrace == 'Wood'):
		plist.append['Longsword','Shortsword','Shortbow','Longbow']
	if pcSubrace == 'Dark':
		plist.append['Rapier','Shortsword','Hand Crossbow']

def getLanguages(pcRace):
	try:
		pcLangList = ("Elvish","Dwarvish","Orcish","Halfling")
		if pcRace == "Human":
			pcLang = [("Common")]
			pcLang.append(random.choice(pcLangList))
		elif pcRace == "Dwarf":
			pcLang = ("Common","Dwarvish")
		elif (pcRace == "Elf") or (pcRace == 'Half-Elf'):
			pcLang = ("Common","Elvish")
		elif pcRace == "Halfling":
			pcLang = ("Common","Halfling")
		elif pcRace == "Dragonborn":
			pcLang = ("Common","Draconic")
		elif pcRace == "Gnome":
			pcLang = ("Common","Gnomish")
		elif pcRace == "Half-Orc":
			pcLang = ("Common","Orc")
		elif pcRace == "Tiefling":
			pcLang = ("Common","Infernal")
		else:
			pcLang = ("Error","No Languages for race defined")
		return pcLang
	except:
		print "ERROR IN GETLANGUAGES"
		return ('Error')


def getAge(pcRace):
	try:
		if pcRace == "Human":
			return random.randint(14,50)
		elif pcRace == "Elf":
			return random.randint(25,500)
		elif pcRace == "Dwarf":
			return random.randint(50,270)
		elif pcRace == "Halfling":
			return random.randint(20,110)
		elif pcRace == "Dragonborn":
			return random.randint(15,80)
		elif pcRace == "Gnome":
			return random.randint(40,400)
		elif pcRace == "Half-Elf":
			return random.randint(20,160)
		elif pcRace == "Half-Orc":
			return random.randint(14,65)
		elif pcRace == "Tiefling":
			return random.randint(14,60)
	except:
		print "ERROR IN GETAGE"
		return 1

def getSpeed(pcRace, pcSubrace):
	if (pcRace == "Dwarf") or (pcRace == 'Gnome'):
		return 25
	elif pcSubrace == "Wood":
		return 35
	else:
		return 30

def getHeightAndWeight(pcRace, pcSubrace):
	'''
	Filled with h/w of corresponding races as of DND5e player guide
	'''
	try:
		if (pcRace == "Human") or (pcRace == "Half-Elf") or pcRace == ("Tiefling"):
			h = (140 + random.randint(5,50))
			w = (50 * (1 + random.random())*1.2)
		elif (pcRace == "Halfling") or (pcRace == 'Gnome'):
			h = (78 + random.randint(5,20))
			w = (22 * (1 + random.random()))
		elif pcSubrace == "Wood":
			h = (130 + random.randint(5,50))
			w = (45 * (1 + random.random())*1.2)
		elif pcSubrace == "Dark":
			h = (125 + random.randint(5,30))
			w = (32 * (1 + random.random())*2.2)
		elif pcSubrace == "High":
			h = (130 + random.randint(5,50))
			w = (48 * (1 + random.random())*1.2)
		elif pcSubrace == "Hill":
			h = (120 + random.randint(5,20))
			w = (52 * (1 + random.random())*2.2)
		elif pcSubrace == "Mountain":
			h = (140 + random.randint(5,20))
			w = (60 * (1 + random.random())*2.2)
		elif pcRace == "Dragonborn":
			h = (170 + random.randint(5,40))
			w = (92 * (1 + random.random())*2.2)
		elif pcRace == "Half-Orc":
			h = (155 + random.randint(5,20))
			w = (65 * (1 + random.random())*2.2)
		return int(h), int(w)
	except:
		print "ERROR IN GETH/W"
		return 0,0

def settings_config(pc_config):
	global newClass, newRace, pcLevel
	if pc_config['use']:
		pcLevel	= pc_config['Level']
		newRace	=	pc_config['Race']
		newClass= 	pc_config['Class']
	else:
		pcLevel =	random.randint(1,4)
		newClass=	None
		newRace =	None


def main():
	'''
	Used to output most data,
	stats and pc data are held in dicts, because it will make it much
	easier to export to other programs, as it will pretty much just be
	"Hey, get this data and print it, yo" and then this prog will be all
	like.. "yea.. lemme get right on dat."
	'''
	global pc


	pc = {}
	pc['Level'] = pcLevel

	pc['Class']					= getStats()

	if newClass is not None:
		if newClass.title() in classesTup:
			pc['Class']	= forceClass(pc['Class'])
	pc['Gender'] = random.choice(('Male','Female'))
	pc['Race'] = getRace(pc['Class'])
	if newRace is not None:
		if newRace.title() in racesTup:
			pc['Race'] = newRace.title()
	pc['Subrace'] = getRaceBonus(pc['Race'])

	pc['strMod'] = getStatModifiers(pc['STR']);pc['dexMod']	= getStatModifiers(pc['DEX'])
	pc['conMod'] = getStatModifiers(pc['CON']);pc['intMod']	= getStatModifiers(pc['INT'])
	pc['wisMod'] = getStatModifiers(pc['WIS']);pc['chrMod']	= getStatModifiers(pc['CHR'])

	pc['Alignment'] = getAlignment(pc['Race'])
	pc['Name'] = getName(pc['Race'], pc['Gender'])
	pc['Speed'] = getSpeed(pc['Race'], pc['Subrace'])
	pc['Age'] = getAge(pc['Race'])
	pc['Lang'] = getLanguages(pc['Race'])
	pc['Height'], pc['Weight'] = getHeightAndWeight(pc['Race'],pc['Subrace'])

	(pc['Trait'], pc['Idea'], pc['Bond'], pc['Flaw'],
		pc['Specilty'], pc['Background'], pc['Feature']) = getBackground(pc['Class'])

	bio = """
BIO:
	Name:	%s
	Gender:	%s
	Race:   %s (%s)
	Class:	%s
	Background:	%s
	Age:	%d	Height:	%dcm
	Align:	%s	Weight:	%dkg
	Lang:	%s

	""" %(pc['Name'], pc['Gender'], pc['Race'],
		pc['Subrace'], pc['Class'], pc['Background'], pc['Age'], pc['Height'], pc['Alignment'], pc['Weight'],
		 ", ".join([str(x) for x in pc['Lang']] )) #to get rid of ugly formatting

	pc['HP']				= getHitPoints(pc['Class'], pc['conMod'], pc['Level'], pc['Subrace'])
	pc['Speed']					= getSpeed(pc['Race'], pc['Subrace'])


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


	pc['Spells'] = getSpells(pc['Class'], pc['Level'])

	def neatListReturn(li):
		s = str()
		for item in li:
			if item != 'None':
				s = s + item + '\n'
			else:
				return 'None\n'
		return s

	spells = str()
	if pc['Spells']:
		spells = spells+"\nCANTRIPS:\n"+neatListReturn(pc['Spells'][0])
		c = 1
		for spell in xrange(0,pc['Level']):
			try:
				spells = spells+'\nLEVEL %d:\n'%c+(neatListReturn(pc['Spells'][c]))
				c += 1
			except: break
	else:
		spells = "\nNo Spells"

	item_d = itemGen.main('wep','rnd')
	weapon = '''
WEAPON:
	Name: 	 %s
	Range:	 %s
	Hit Die: 	%s
	Dam Type:	%s

	'''%(item_d['Name'],item_d['Weapon Type'],
		item_d['Hit Die'],item_d['Damage Type'])

	armor_d = itemGen.main('arm','rnd')
	armor = '''
ARMOR:
	Name:	%s
	Type:	%s
	AC:	%s
	Cost:	%s
	'''%(armor_d['Name'],armor_d['Type'],
		armor_d['AC'],armor_d['Cost'])


	background = '''
BACKGROUND:
TRAITS:\n%s

IDEAL:\n%s

BOND:\n%s

FLAW:\n%s

SPECIALTY:\n%s

FEATURE:\n%s
	'''%(pc['Trait'], pc['Idea'],
		pc['Bond'], pc['Flaw'], pc['Specilty'], pc['Feature'])

	pc['Info'] = bio+stats+weapon+armor+spells+background
	if pc['Class'] == 'Commoner':
		pc['Info'] = bio+stats
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
