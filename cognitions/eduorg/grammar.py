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
from natasha.data import load_dict

from natasha.grammars.name import SIMPLE_NAME
from natasha.grammars.person import POSITION_NAME

from yargy.rule.transformators import RuleTransformator


class StripInterpretationTransformator(RuleTransformator):
    def visit_InterpretationRule(self, item):
        return self.visit(item.rule)

NAME = SIMPLE_NAME.transform(StripInterpretationTransformator)
PERSON = POSITION_NAME.transform(StripInterpretationTransformator)

### NATASHA EXTRACTOR DEF
from natasha.extractors import Extractor
class eduorgExtractor(Extractor):
    def __init__(self):
        super(eduorgExtractor, self).__init__(EDUORG)  
###
import re
from  lib.func import get_dictPath, load_regex
EDUORG_DICT = dictionary(set(load_dict(get_dictPath('eduorg', 'dict_main.txt'))))
EDUORG_DICT_REGEXP = re.compile(load_regex(get_dictPath('eduorg', 'dict_main.txt')))

## 1 - FACT INIT
eduorg = fact('eduorg', ['name'])
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
            custom(lambda s: EDUORG_DICT_REGEXP.search(s), types=(str))
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
   EDUORG_DICT,
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
    EDUORG_DICT,
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
      EDUORG_DICT,      
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
).interpretation(eduorg.name.normalized())


###

### SUMMARY RULE
EDUORG_ = or_(
  INTERPRET_NAME,
)
###

### EXPORT RULE
EDUORG = EDUORG_.interpretation(
    eduorg.name
).interpretation(
    eduorg
)
###
