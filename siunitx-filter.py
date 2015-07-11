#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Pandoc filter to use numbers with physical units.

In markdown you should write NUMBER{UNIT}.
Ex: 10{ms}, 2.6{GHz}, etc

The filter will then separate the number and the unit.

In latex it will be replaced with \SI{NUMBER}{UNIT};

In HTML the number + unit will inside a span tag with "phy-quantity" class,
the number alone will be in a span tag with "phy-number" class and the unit
will be in a span tag with "phy-unit" tag. You can then edit your CSS as
desired to, for instance, add a small left margin to the phy-unit class.

For all the other formats "NUMBER{UNIT}" will be replaced with "NUMBER
UNIT".
"""

from pandocfilters import toJSONFilter, Str, RawInline
import re


# Match something such as '10{ms}', 30{Htz}, etc.
# The regex will catch two groups. the first group is the number and the
# second group is the unit.
pattern = re.compile(
    ('(\d+\.?\d*'  # Match either float numbers ...
     '|'           # or ...
     '\d+\.?\d*[eE][+-]\d+)'  # numbers in scientific notation
     '{(.+?)}')  # Followed by the unit inside {}
)


def replace_unit(key, value, format, meta):
    """
    Try to perform the replacements in `value` according to `pattern`.

    If nothing is replaced the this function does not return any value. If
    a replacement is performed then a `RawInline` object is returned to
    pandoc.

    Parameters
    ----------

    key : (string) The pandoc element type. Here we check if it is 'Str'.

    value : (string) The original text.
    format : (string) The output format of pandoc.
    meta : Not used here.
    """
    if key == 'Str':
        if format == 'html' or format == 'html5':
            replacement = ("<span class=\"phy-quantity\">"
                           # First regex group is the number
                           "<span class=\"phy-number\">\\1</span>"
                           # First regex group is the unit
                           "<span class=\"phy-unit\">\\2</span>"
                           "</span>")
            newValue = pattern.sub(replacement, value)
            if newValue != value:
                return RawInline("html", newValue)

        elif format == 'latex':
            replacement = "\\SI{\\1}{\\2}"
            newValue = pattern.sub(replacement, value)
            if newValue != value:
                return RawInline("latex", newValue)


if __name__ == "__main__":
    toJSONFilter(replace_unit)
