#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  questGen.py
#
#  Copyright 2014 Tyler Dinsmoor <d@d-netbook>

import random
import itemGen

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

class Quest():
    import npcGen
    npc = npcGen.NPC()
    def __init__(self, owner="Bob the Builder"):
        self.quest_owner = owner
        self.quest_type()
        self.get_reward()
        self.quest_description()
        
    def quest_description(self):
        self.quest_introduction = "Hello, my name is %s.\n"%self.quest_owner
        self.quest_summary = """Now that you mention it, I sure could
use some help %s...
Interested?
"""%(self.quest_theme)
        self.quest_desc = (self.quest_introduction + self.quest_summary +
            self.quest_dialog + self.quest_reward)

    def quest_type(self):
        #I need help X
        types = {
            'finding a specific item':self.find_item,
            'retrieving a stolen item':self.retrive_item,
            'getting information from someone':self.get_information,
            'rescuing a captive':self.rescue_captive,
            'finding out what happened to my friend':self.find_friend,
            'killing a monster':self.kill_monster,
            'figuring out a strange phenomenon':self.anomaly,
            'getting an individual to help me':self.person_help,
            }
        self.quest_theme = random.choice(types.keys())
        types[self.quest_theme]()
        #self.person_help()
        
    
    def find_item(self):
        self.quest_dialog = "It's rumored there is a special %s laying in the forest."%(
        itemGen.rand_item()['name'])
        
    
    def retrive_item(self):
        self.quest_dialog = "%s stole my %s! %s"%(
        self.npc.npcinfo['name'],itemGen.rand_item()['name'],
        self.npc.npcdesc[0])
    
    def get_information(self):
        topics = (
            'why they were in my house',
            'where they were last week',
            'when the last time they wrote their mother',
            'how they got out of prison',
            'where they got their wealth',
            'whoever taught them to fight',
            'strange magic in the region',
            'noises around their residence',
            'strange nightly visitation',
            'seeing me soon',
            'why they want me dead',
            )
            
        self.quest_dialog = "Investigate %s about %s.\nIt's very important.\n%s"%(
        self.npc.npcinfo['name'],random.choice(topics),self.npc.npcdesc[0])
    
    def rescue_captive(self):
        import npcGen
        captor = npcGen.NPC()
        places = (
            'castle',
            'dungeon',
            'keep',
            'mud hut',
            'back room of an Inn',
            'residence closet',
            'jail',
            'outhouse',
            'mobile wagon',
            )
            
        directions = ('north','south','east','west')
        
        self.quest_dialog = "My friend %s is being kept against their will\nin a %s to the %s by %s, a %s\nPlease set them free!"%(
        self.npc.npcinfo['name'], random.choice(places), random.choice(directions), captor.npcinfo['name'],captor.npcdesc[0])
        
    def find_friend(self):
        last_place = (
            'their house',
            'the brothel',
            'the Inn',
            'the corner store',
            'their back yard',
            'the clearing in the forest',
            'brewery',
            'their workplace',
            'the guard towers',
            'alley behind my place',
            "their 'friends place'",
            )
        self.quest_dialog = "My good friend %s has been missing for %d days.\nThe last place I saw them was at %s. They look like a %s\nCould you find out what happened to them?"%(
        self.npc.npcinfo['name'], random.randint(1,20),random.choice(last_place), self.npc.npcdesc[0])
    
    def kill_monster(self):
        import monGen
        mon = monGen.Monster().mon
        
        problems = (
            'killing livestock',
            'destroying houses',
            'killing farmers',
            'raiding caravans',
            'looting store rooms',
            'singing obnoxiosuly',
            'being an ugly bastard',
            'stealing',
            'making fun of me',
            'attacking civilians',
            'ambushing adventurers',
            )
        
        self.quest_dialog = "Damn %s keeps %s. Needs to stop."%(mon['name'], random.choice(problems))
        
    def anomaly(self):
        places = (
            'the kitchen of the inn',
            'the bookstore',
            'the place two buildings down',
            'southern district square',
            'my friends office',
            'my ironworking facility',
            'a local brothel',
            'the streets in front of town hall',
            'my daughters house',
            'the coal mine',
            )
        stranges = (
            'floating lights',
            'a stench of death',
            'ghostly figures',
            'people turning invisible',
            'whispers from nowhere',
            'people losing their coinpurses',
            'objects deforming',
            'Imp attacks',
            'intense pain being inflicted',
            'people getting sick',
            'booming voices',
            'a strange odor',
            'singing from the walls',
            'fires erupting',
            )
        self.quest_dialog = "Strange things have been happening at %s.\nSomething about %s...?"%(
        random.choice(places),random.choice(stranges))
        
    
    def person_help(self):
        helpdo = (
            'manage my finances',
            'wash my house',
            'join that local cult',
            '"take care" of our neighbor',
            'plan an uprising',
            'cook a grand meal',
            'repair my roof',
            'hunt for this season',
            'contribute to the community',
            'campaign for a political figure',
            'carry this heavy trunk to the market',
            'marry their sibling',
            )
        
        self.quest_dialog = "Get that scoundrel %s to help me %s."%(
        self.npc.npcinfo['name'], random.choice(helpdo))
    
    
    def get_reward(self):
        rewards = {
            'very easy':str(random.randint(20,100))+'sp',
            'easy':str(random.randint(2,20))+'gp',
            'medium':str(random.randint(20,50))+'gp',
            'hard':str(random.randint(50,100))+'gp',
            'very hard':str(random.randint(120,400))+'gp',
            'nearly impossible':str(random.randint(500,700))+'gp',
            }
        diff = random.choice(rewards.keys())
        self.quest_reward = "\nThis is a %s task, which will be rewarded\nwith %s worth of goods."%(
        diff,rewards[diff])
