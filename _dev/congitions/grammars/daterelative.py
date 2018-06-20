# coding: utf-8
from __future__ import unicode_literals
from yargy import (rule, fact, not_, and_, or_, attribute,)
from yargy.predicates import (gram, caseless, normalized, is_title, dictionary, custom,)
#from yargy.relations import (gnc_relation, case_relation,)

## 1 - FACT INIT
DateRelative = fact('DateRelative', ['name'])
from natasha.dictionaries.daterelative import DATERELATIVE_DICT
###

### 2 - INIT GRAMS & GRAM RULES (pymorphy2)
ADJF = gram('ADJF')
NOUN = gram('NOUN')
INT = gram('INT')
TITLE = is_title()

###


### 1-ST RING RULES
R1_SIMPLE = rule(
   DATERELATIVE_DICT,
).repeatable()
###


### 2-ST RING RULES

###
    
### INTERPRETATION RULE
INTERPRET_NAME = rule(or_(
  R1_SIMPLE,  
  )
).interpretation(DateRelative.name.normalized())
###

### SUMMARY RULE
DATERELATIVE_ = or_(
  INTERPRET_NAME,
)
###

### EXPORT RULE
DATERELATIVE = DATERELATIVE_.interpretation(DateRelative)
###
