# coding: utf-8
from __future__ import unicode_literals
from yargy import (rule, fact, not_, and_, or_, attribute,)
from yargy.predicates import (gram, caseless, normalized, is_title, dictionary, custom, eq, )
from yargy.relations import (gnc_relation, case_relation,)

### NATASHA EXTRACTOR DEF
from natasha.extractors import Extractor
class _tmplExtractor(Extractor):
    def __init__(self):
        super(_tmplExtractor, self).__init__(_TMPL)  
###

## 1 - FACT INIT
_tmpl = fact('_tmpl', ['name', 'tmp', 'tmp2'])
from .dictionary import _TMPL_DICT, _TMPL_DICT_REGEXP
###

### 2 - INIT GRAMS & GRAM RULES (pymorphy2)
ADJF = gram('ADJF')
NOUN = gram('NOUN')
INT = gram('INT')
TITLE = is_title()


#ADJF
ADJF_PREFIX_ADJF = and_(
    ADJF,
    TITLE
).repeatable()

ADJF_NORM = rule(
            and_(
            ADJF,
            custom(lambda s: _TMPL_DICT_REGEXP.search(s), types=(str))
            )
).repeatable()

#
###


### 1-ST RING RULES
R1_SIMPLE = rule(
   _TMPL_DICT,
).repeatable()


R1_ADJF = rule(
   ADJF_NORM,
).repeatable()
###


### 2-ST RING RULES
R2_SIMPLE_W_ADJF = rule(
    ADJF_PREFIX,
    R1_SIMPLE,
).repeatable()


R2_QUOTED = or_(rule(
    _TMPL_DICT,
    gram('QUOTE'),
    not_(
        or_(
            gram('QUOTE'),
            gram('END-OF-LINE'),
        )).repeatable(),
    gram('QUOTE')),
    
    rule(
      gram('QUOTE'),
      ADJF.optional(),      
      _TMPL_DICT,      
      not_(
          or_(
              gram('QUOTE'),
              gram('END-OF-LINE'),
          )).repeatable(),
      gram('QUOTE'),        
))

###
    
### INTERPRETATION RULE
INTERPRET_NAME = rule(or_(
  R2_QUOTED,
  R2_SIMPLE_W_ADJF,
  R1_SIMPLE,  
  )
).interpretation(_tmpl.name.normalized())
###

### SUMMARY RULE
_TMPL_ = or_(
  INTERPRET_NAME,
)
###

### EXPORT RULE
_TMPL = _TMPL_.interpretation(_tmpl)
###
