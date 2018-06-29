# coding: utf-8
from __future__ import unicode_literals
from yargy import (rule, fact, not_, and_, or_, attribute,)
from yargy.predicates import (eq, in_, true, gram, caseless, normalized, is_capitalized, is_single, is_title, dictionary,)
from yargy.relations import (gnc_relation, case_relation,)
from natasha.data import load_lines
from yargy.pipelines import MorphPipeline

## FACT INIT
EduOrganisation = fact('EduOrganisation', ['name'])
from natasha.dictionaries.eduorganisation import EDUORGANISATION_DICT
###

class TestTypePipeline(MorphPipeline):
    grammemes = {'test'}
    keys = [
        'университет',
    ]
TEST = gram('test')

### GRAM RULES (pymorphy2)
ADJF = gram('ADJF')
NOUN = gram('NOUN')
INT = gram('INT')
ADVB = gram('ADVB')
POST = gram('POST')
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
).repeatable()

ADJF_PREFIX_ADJF = and_(
    ADJF,
    TITLE
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
   EDUORGANISATION_DICT,
).repeatable()

gnc = gnc_relation()
R1_SIMPLE_ADVB_2 = and_(
    ADJF,
    TEST
)

R1_SIMPLE_ADVB = rule(
    R1_SIMPLE_ADVB_2.match(gnc).interpretation(
        EduOrganisation.name.inflected()
    ))



### 2-ST RING RULES
#Кембриджском университете
#Казанский и Московский университеты
R2_SIMPLE_W_ADJF = rule(
    ADJF_PREFIX,
    R1_SIMPLE,
).repeatable()

R2_QUOTED = or_(rule(
    EDUORGANISATION_DICT,
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
      EDUORGANISATION_DICT,      
      not_(
          or_(
              gram('QUOTE'),
              gram('END-OF-LINE'),
          )).repeatable(),
      gram('QUOTE'),        
))
        
R2_KNOWN = rule(
    gram('Orgn'),
    GENT_GROUP,
)
###
    
### INTERPRETATION RULE
INTERPRET_NAME = rule(or_(
  #R2_QUOTED,
  #R2_SIMPLE_W_ADJF,
  #R2_KNOWN,
  #R1_SIMPLE,  
  R1_SIMPLE_ADVB
  )
).interpretation(EduOrganisation.name.normalized())


###

### SUMMARY RULE
EDUORGANISATION_ = or_(
  INTERPRET_NAME,
)
###

### EXPORT RULE
EDUORGANISATION = EDUORGANISATION_.interpretation(EduOrganisation)
###
