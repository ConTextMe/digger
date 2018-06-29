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


name = 'name'

def factData(args, session, match):
    data = {
      "fname" : match.fact.first,
      "lname" : match.fact.last,
      "mname" : match.fact.middle  
      }
    return data


def visualSettings():
  extractors = {}; extractors['color'] = "#0713ff"; extractors['opacity'] = "0.2"
  return extractors
