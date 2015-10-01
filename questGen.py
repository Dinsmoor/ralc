#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  questGen.py
#
#  Copyright 2014 Tyler Dinsmoor <d@d-netbook>

import random

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

'''
Quest Requirements:
    Theme
    Difficulty
    Rewards
    Location
    NPCs

'''
class Quest(object):
    def __init__(self, actors):
        pass

    def get_reward(self, reward):
        pass

    def get_completion_requirements(self, reqire_list):
        pass

    def quest_description(self):
        print "Generic Quest"

class LootQuest(Quest):
    "Go hunt down this lost treasure"
    def __init__(self):
        Quest.quest_description(self)
    pass

class TheftQuest(LootQuest):
    "Silently Steal an item"
    pass

class MugQuest(LootQuest):
    "Mug person for item"
    pass


class LocateObjectQuest(Quest):
    "Locate an object"
    pass


class LocatePersonQuest(Quest):
    "Locate an person"
    pass

class RescueQuest(LocatePersonQuest):
    "Locate and rescure NPC"
    pass


class KillQuest(Quest):
    "Kill Someone/something"
    pass

class MurderQuest(KillQuest):
    "Kill person violently"
    pass

class AssasinateQuest(KillQuest):
    "Kill person Silently"
    pass


class UprisingQuest(Quest):
    "Cause a village to revolt"
    pass

class DefendQuest(Quest):
    "Fight back invading force"
    pass


LootQuest()

def main():
    return

if __name__ == '__main__':
    import def_settings
    default_settings = def_settings.get_def_settings()
    main()

