# coding: utf-8
from __future__ import unicode_literals

from yargy import (
    rule,
    and_, or_,
    fact
)
from yargy.predicates import (
    eq, gte, lte,
    dictionary, normalized
)


Date = fact(
    'Date',
    ['year', 'month', 'day']
)


MONTHS = {
    'январь': 1,
    'февраль': 2,
    'март': 3,
    'апрель': 4,
    'май': 5,
    'июнь': 6,
    'июль': 7,
    'август': 8,
    'сентябрь': 9,
    'октябрь': 10,
    'ноябрь': 11,
    'декабрь': 12,
}


MONTH_NAME = dictionary(MONTHS).interpretation(
    Date.month.normalized()
)

MONTH = and_(
    gte(1),
    lte(12)
).interpretation(
    Date.month
)

DAY = and_(
    gte(1),
    lte(31)
).interpretation(
    Date.day
)

YEAR_WORD = or_(
    rule('г', eq('.').optional()),
    rule(normalized('г.'), eq('.').optional()),
    rule(normalized('год')),
    rule(normalized('гг')),
    rule(')'),
)
YEAR_PREFIX = or_(
    rule('в '),
    rule('c '),
    rule(', '),
    rule('('),
)

YEAR_POSTFIX = or_(
    rule('е'),
    rule('го'),
    rule('ым'),
    rule('м'),
)

YEAR_COUPLE = or_(
    rule('-'),
    rule(','),
).repeatable()

YEAR = and_(
    gte(1200),
    lte(2100)
).interpretation(
    Date.year
)

YEAR_SHORT = and_(
    gte(0),
    lte(99)
).interpretation(
    Date.year
)

DATE = or_(
    rule(
        DAY,
        '.',
        MONTH,
        '.',
        or_(
            YEAR,
            YEAR_SHORT
        ),
        YEAR_WORD.optional()
    ),
    rule(
        YEAR,
        YEAR_WORD
    ),
    rule(
        YEAR,
        '-',
        YEAR_POSTFIX,
        YEAR_WORD.optional()
    ),
    rule(
        YEAR,
        '\n',
        YEAR_WORD
    ),
    rule(
        YEAR_PREFIX,
        YEAR
    ),    
    rule(
        YEAR,
        YEAR_COUPLE,
        YEAR,
        YEAR_WORD.optional()
    ),   
    rule(
        YEAR_PREFIX,
        YEAR,
        YEAR_COUPLE,
        YEAR_WORD.optional()
    ),         
    rule(
        DAY,
        MONTH_NAME
    ),
    rule(
        MONTH_NAME,
        YEAR,
        YEAR_WORD.optional()
    ),
    rule(
        DAY,
        MONTH_NAME,
        YEAR,
        YEAR_WORD.optional()
    ),
).interpretation(
    Date
)
