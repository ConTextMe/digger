# -*- coding: utf-8 -*-
########    #######    ########    #######    ########    ########
##     / / / /    License    \ \ \ \ 
##    Copyleft culture, Copyright (C) is prohibited here
##    This work is licensed under a CC BY-SA 4.0
##    Creative Commons Attribution-ShareAlike 4.0 License
##    Refer to the http://creativecommons.org/licenses/by-sa/4.0/
########    #######    ########    #######    ########    ########
##    / / / /    Code Climate    \ \ \ \ 
##    Language = python3
##    Indent = space;    2 chars;
########    #######    ########    #######    ########    ########


cname = 'eduorg'

def factData(args, session, match):
    data = {
      cname + "_name" : match.fact.name
      }
    return data


def visualSettings():
  extractors = {}; extractors['color'] = "#0713ff"; extractors['opacity'] = "0.2"
  return extractors
