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


from __future__ import unicode_literals
from yargy import (rule, not_, and_, or_, )
#attribute
from yargy.predicates import (gram, caseless, normalized, is_title, dictionary, custom, eq, in_, is_capitalized,)
from yargy.relations import (gnc_relation, case_relation,)
from yargy.interpretation import fact
from yargy.tokenizer import QUOTES
#from .name import (
    #Name,

    #FIRST_LAST,
    #LAST_FIRST,
    #TITLE_FIRST_LAST,
    #TITLE_LAST_FIRST,

    #ABBR_FIRST_LAST,
    #LAST_ABBR_FIRST,
    #ABBR_FIRST_MIDDLE_LAST,
    #LAST_ABBR_FIRST_MIDDLE,

    #TITLE_FIRST_MIDDLE,
    #TITLE_FIRST_MIDDLE_LAST,
    #TITLE_LAST_FIRST_MIDDLE,

    #JUST_FIRST,
    #JUST_LAST
#)
### NATASHA EXTRACTOR DEF
from natasha.extractors import Extractor
class personExtractor(Extractor):
    def __init__(self):
        super(personExtractor, self).__init__(PERSON)  
###

## 1 - FACT INIT
person = fact('person', ['name'])
from .dictionary import PERSON_DICT, PERSON_DICT_REGEXP
###

### 2 - INIT GRAMS & GRAM RULES (pymorphy2)
ADJF = gram('ADJF')
NOUN = gram('NOUN')
INT = gram('INT')
TITLE = is_title()

PRE_WORDS = rule(
  or_(
    or_(
      gram('PREP'),
      gram('Vpre'),
      gram('CONJ'),
      gram('PRCL'),
      gram('INTJ'),
    ),
    gram('POST'),    
  ).optional()
)
    
case = case_relation()
GENT_GROUP = rule(
    gram('gent').match(case)
).repeatable().optional()

#ADJF
ADJF_PREFIX_COUNTABLE = rule(
    or_(caseless('и'), eq(',')).optional(),
)


ADJF_PREFIX_ADJF = and_(
    ADJF,
    TITLE
).repeatable()


ADJF_NORM = rule(
            and_(
            ADJF,
            custom(lambda s: PERSON_DICT_REGEXP.search(s), types=(str))
            )
).repeatable()


ADJF_PREFIX = rule(
    ADJF_PREFIX_ADJF,
    ADJF.optional(), #Киевском государственном университете
    ADJF_PREFIX_COUNTABLE
).repeatable()
#
###


### 1-ST RING RULES
R1_SIMPLE = rule(
   PERSON_DICT,
).repeatable()


R1_ADJF = rule(
   ADJF_NORM,
).repeatable()
###


### 2-ST RING RULES

#Кембриджском университете
#Казанский и Московский университеты
R2_SIMPLE_W_ADJF = rule(
    ADJF_PREFIX,
    R1_SIMPLE,
).repeatable()


R2_QUOTED = or_(rule(
    PERSON_DICT,
    in_(QUOTES),
    not_(
        or_(
            in_(QUOTES),
            #gram('END-OF-LINE'),
        )).repeatable(),
    in_(QUOTES)),
    
    rule(
      in_(QUOTES),
      ADJF.optional(),      
      PERSON_DICT,      
      not_(
          or_(
              in_(QUOTES),
              #gram('END-OF-LINE'),
          )).repeatable(),
      in_(QUOTES),        
))


R2_KNOWN = rule(
    gram('Orgn'),
    GENT_GROUP,
)
###
    
### INTERPRETATION RULE
INTERPRET_NAME = rule(or_(
  R2_QUOTED,
  R2_SIMPLE_W_ADJF,
  R2_KNOWN,
  R1_SIMPLE,  
  )
).interpretation(person.name.normalized())


###

### SUMMARY RULE
PERSON_ = or_(
  INTERPRET_NAME,
)
###

### EXPORT RULE
PERSON = PERSON_.interpretation(person)
###
