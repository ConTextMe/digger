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


cname = 'date'

def factData(args, session, match):
    data = {
      cname + "_year" : match.fact.year,
      cname + "_month"  : match.fact.month,
      cname + "_day"   : match.fact.day  
      }
    return data


def visualSettings():
  extractors = {}; extractors['color'] = "#0713ff"; extractors['opacity'] = "0.2"
  return extractors
