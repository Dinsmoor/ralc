#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  monGen.py
#  
#  Copyright 2016 Tyler Dinsmoor <pappad@airmail.cc>
#  

import random
from markovnames import nameGen

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

class NPC:
    def __init__(self):
        self.npcinfo = dict()
        self.npcdesc = dict()
        self.npcinfo['gender'] = random.choice(("male","female"))
        self.race()
        self.name()
        self.appearance()
        self.abilities()
        self.talents()
        self.mannerisms()
        self.interaction_traits()
        self.ideals()
        self.bonds()
        self.flaws()
        self.quest()
        #print self.npcinfo
        self.build_desc()
        self.describe_me()

    def describe_me(self):
        self.desc = str()
        for desc in self.npcdesc.itervalues():
            self.desc += desc + "\n"

    def build_desc(self):
        npcinfo = self.npcinfo
        npc_privacy = random.randint(1,25)
        npc_age = random.choice(('young','adult','mature','aged','elderly'))
        pronouns = {
                'male':('him','he'),
                'female':('her','she'),
                }
        npc_pronoun = pronouns[npcinfo['gender']]
        self.npcdesc[0] = '''
A %s %s %s, %s has %s.
%s appears %s, but also seems %s.
            '''%(npc_age,npcinfo['gender'],npcinfo['race'],
            npc_pronoun[1],npcinfo['appearance'],npc_pronoun[1].capitalize(),
            npcinfo['abil_high_desc'],npcinfo['abil_low_desc'])
        self.npcdesc[1] = '''
%s introduces %sself as %s.
A short chat reveals that %s is %s,
and is quite %s.
        '''%(npc_pronoun[1].capitalize(), npc_pronoun[0], npcinfo['name'],
        npc_pronoun[1], npcinfo['talent'],npcinfo['traits'])

        self.npcdesc[2] = '''
Further communications with %s reveals that
%s %s, which you take note.
        '''%(npcinfo['name'],npc_pronoun[1],npcinfo['mannerisms'])

        self.npcdesc[3] = '''
Time spent with %s makes it clear that %s is
a generally %s person, who has strong beliefs in %s.
        '''%(npcinfo['name'],npc_pronoun[1],npcinfo['alignment'],npcinfo['ideal'])

        self.npcdesc[4] = '''
Either through spying, or becoming a good friend, it has become known
to you that %s is %s.
You also learn %s is plauged by %s.
        '''%(npcinfo['name'], npcinfo['bond'],npc_pronoun[1], npcinfo['flaw'])
        
        self.npcdesc[5] = "SIDE-QUEST:\n" + self.npcinfo['quest']

    def race(self):
        self.npcinfo['race']= random.choice(('human', 'elf', 'dwarf', 'halfling', 'half-elf', 'half-orc',
            'dragonborn', 'gnome'))

    def name(self):
            names = get_f_f_lol('data/char/' + (self.npcinfo['race'].lower() + 'Names'))
            if self.npcinfo['race'] == 'half-orc':
                # half-orcs don't have last names
                ln = ''
            else:
                ln = nameGen.get_name(names[2])
            if self.npcinfo['gender'] == 'male':
                fn = nameGen.get_name(names[0])
            else:
                fn = nameGen.get_name(names[1])
            self.npcinfo['name'] = fn + ' ' + ln

    def appearance(self):
        self.npcinfo['appearance'] = random.choice((
                    'distinctive jewlery',
                    'piercings',
                    'some outlandish clothing',
                    'formal, clean clothes',
                    'ragged, dirty clothes',
                    'a pronounced scar',
                    'some missing teeth',
                    'some missing fingers',
                    'an unusual eye color',
                    'tattoos',
                    'birthmarks',
                    'an unusual skin color',
                    'a bald head',
                    'braided hair',
                    'an unusual hair color',
                    'a nervous eye twitch',
                    'a distinctive nose',
                    'a distinctive posture',
                    'the gift of being exceptionally beautiful',
                    'the curse of being exceptionally ugly'
                    ))

    def abilities(self):
        #           Stat, hidesc, lodesc
        abilities = {'Strength':(('powerful', 'brawny'),('feeble', 'scrawny')),
                    'Dexterity':(('lithe', 'agile', 'graceful'),('clumsy', 'fumbling')),
                    'Constitution':(('hardy', 'hale', 'healthy'),('sickly', 'pale')),
                    'Intelligence':(('studious', 'learned', 'inquisitive'),('dim-witted', 'slow')),
                    'Wisdom':(('perceptive', 'spiritual', 'insightful'),('oblivious', 'absent-minded')),
                    'Charisma':(('persuasive', 'forceful', 'born leader'),('dull', 'boring'))}

        self.npcinfo['abil_high'],self.npcinfo['abil_low'] = random.sample(abilities.keys(), 2)
        self.npcinfo['abil_high_desc'] = random.choice(abilities[self.npcinfo['abil_high']][0])
        self.npcinfo['abil_low_desc'] = random.choice(abilities[self.npcinfo['abil_low']][1])

    def talents(self):
        self.npcinfo['talent'] = random.choice((
                        'good at playing a musical instument',
                        'able to speak several languages fluently',
                        'unbelievably lucky',
                        'gifted with a perfect memory',
                        'great with animals',
                        'great with children',
                        'great at solving puzzles',
                        'great at (one game)',
                        'great at impersonations',
                        'known for drawing beautifully',
                        'known for painting beautifully',
                        'known for singing beautifully',
                        'known for drinking everyone under the table',
                        'an expert carpenter',
                        'an expert cook',
                        'an expert dart thrower and rock skipper',
                        'an expert juggler',
                        'a skilled actor and master of disguise',
                        'a skilled dancer',
                        ))

    def mannerisms(self):
        self.npcinfo['mannerisms'] = random.choice((
                            'is prone to singing, whistling, or humming quietly',
                            'speaks in rhyme or some other peculiar way',
                            'has a particularly low or high voice',
                            'slurs words, lisps, or stutters',
                            'enunciates overly clearly',
                            'speaks loudly',
                            'whispers',
                            'uses flowery speach or long words',
                            'frequently uses the wrong word',
                            'uses colorful oaths and exclamations',
                            'makes constant jokes or puns',
                            'is prone to declarations of doom',
                            'fidgets',
                            'squints',
                            'stares into the distance',
                            'chews something',
                            'paces',
                            'taps fingers',
                            'bites fingernails',
                            'twirls hair or tugs beard',
                            ))

    def interaction_traits(self):
        self.npcinfo['traits'] = random.choice((
                            'argumentative',
                            'arrogant',
                            'blustering',
                            'rude',
                            'curious',
                            'friendly',
                            'honest',
                            'hot tempered',
                            'irritable',
                            'ponderous',
                            'quiet',
                            'suspicious',
                            ))

    def ideals(self):
        ideals = {      'good':('beauty','charity','greater good','life','respect','self-sacrifice'),
                        'evil':('domination','greed','might','pain','retribution','slaughter'),
                        'lawful':('community','fairness','honor','logic','responsibility','tradition'),
                        'chaotic':('change','creativity','freedom','independence','no limits','being whimsy'),
                        'neutral':('balance','knowledge','live and let live','moderation','neutrality','people'),
                        'nonaligned':('aspiration','discovery','glory','a strong nation','redemption','self-knowledge'),
                    }
        self.npcinfo['alignment'] = random.choice(ideals.keys())
        self.npcinfo['ideal'] = random.choice(ideals[self.npcinfo['alignment']])

    def bonds(self):
        bonds = (
                'dedicated to fulfilling a personal life goal',
                'protective of close family members',
                'protective of colleagues or compatriots',
                'loyal to a benefactor, patron, or employer',
                'captivated by a romantic interest',
                'drawn to a special place',
                'protective of a sentimental keepsake',
                'protective of a valuable possesion',
                'out for revenge',
                )
        self.npcinfo['bond'] = random.choice(bonds)

    def flaws(self):
        flaws = (
                'a forbidden love',
                'a susceptibility to romance',
                'enjoying decadent pleasures',
                'arrogance',
                'an envy for another creature`s possessions',
                'an envy for another creature`s station',
                'overpowering greed',
                'a tendancy to rage',
                'a powerful enemy',
                'a specific phobia',
                'a shameful or scandalous history',
                'a secret crime or misdeed',
                'possession of forbidden lore',
                'foodlhardy bravery',
                )
        self.npcinfo['flaw'] = random.choice(flaws)
        
    def quest(self):
        if random.randint(0,4) == 0:
            import questGen
            self.npcinfo['quest'] = questGen.Quest(owner=self.npcinfo['name']).quest_desc
        else: self.npcinfo['quest'] = "No, I have no need of help."
