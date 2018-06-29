# coding: utf-8
from __future__ import unicode_literals

from yargy import (
    rule, fact,
    or_
)
from yargy.predicates import gram
from yargy.pipelines import MorphPipeline

from .name import (
    Name,

    FIRST_LAST,
    LAST_FIRST,
    TITLE_FIRST_LAST,
    TITLE_LAST_FIRST,

    ABBR_FIRST_LAST,
    LAST_ABBR_FIRST,
    ABBR_FIRST_MIDDLE_LAST,
    LAST_ABBR_FIRST_MIDDLE,

    TITLE_FIRST_MIDDLE,
    TITLE_FIRST_MIDDLE_LAST,
    TITLE_LAST_FIRST_MIDDLE,

    JUST_FIRST,
    JUST_LAST
)






POSITION = gram('Position')

GENT = gram('gent')

WHERE = or_(
    rule(GENT),
    rule(GENT, GENT),
    rule(GENT, GENT, GENT),
    rule(GENT, GENT, GENT, GENT),
    rule(GENT, GENT, GENT, GENT, GENT),
)

POSITION = rule(
    POSITION,
    WHERE.optional()
).interpretation(
    Person.position
)

COMPLEX = or_(
    FIRST_LAST,
    LAST_FIRST,
    TITLE_FIRST_LAST,
    TITLE_LAST_FIRST,

    ABBR_FIRST_LAST,
    LAST_ABBR_FIRST,
    ABBR_FIRST_MIDDLE_LAST,
    LAST_ABBR_FIRST_MIDDLE,

    TITLE_FIRST_MIDDLE,
    TITLE_FIRST_MIDDLE_LAST,
    TITLE_LAST_FIRST_MIDDLE,
).interpretation(
    Name
).interpretation(
    Person.name
)

SIMPLE = or_(
    JUST_FIRST,
    JUST_LAST
).interpretation(
    Name
).interpretation(
    Person.name
)

PERSON_ = or_(
    rule(
        POSITION
        #POSITION.optional(),
        #COMPLEX
    ),
    SIMPLE
)

PERSON = PERSON_.interpretation(
    Person
)
