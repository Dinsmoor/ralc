#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  def_settings.py
#
#  Copyright 2015 Tyler Dinsmoor <pappad@airmail.cc>
#

def get_def_settings():
    char_setting = {
        'use':False,
        'Level':1,
        'Class':'Commoner',
        'Race':None,
            }
    
    map_setting = {
                'biome':None,
                }
    town_settings = {
                'size_mod': 1.0,
                'affluence': 0.8,
                'resources':[],
                'govt':None,
                }
    
    party_setting = {
                'Billy':5,
                'Bob':4,
                }
    
    default_settings = {
            'char':char_setting,
            'map':map_setting,
            'town':town_settings,
            'party':party_setting
                    }
    return default_settings

