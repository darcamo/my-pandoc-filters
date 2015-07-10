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
     '\d+\.?\d*[eE][+-]\d+)'  # scientific notation
     '{(.+?)}')  # Followed by the unit inside {}
)

def caps(key, value, format, meta):
    if key == 'Str':
        m = pattern.search(value)
        if m:
            # Start of the string (before the match). As an example, if
            # value is "(1.3{ms})." the match will find "1.3{ms}" and start
            # will be "(".
            start = value[:m.start()]
            # Continuing the previous example, end will be ")."
            end = value[m.end():]
            number = m.group(1)
            unit = m.group(2)

            # Note that sometimes the regex will match with a 'start' that
            # we don't want. Ex: In "127.0.0.0{IP}" it will match the final
            # "0.0{IP}". But for now we are not handling these cases.
            
            if format == 'html':
                # The whole number with unit is surrounded by a
                # "phy-quantity" span. The number if surrounded by a
                # "phy-number" span and the unit is surrounded by a
                # "phy-unit" span
                return RawInline(
                    "html",
                    start +
                    "<span class=\"phy-quantity\">" +
                    "<span class=\"phy-number\">" + number.strip() +
                    "</span>" +  # End of phy-number span
                    "<span class=\"phy-unit\">" + unit.strip() +
                    "</span>" +  # End of phy-unit span
                    "</span>" +  # End of phy-quantity span
                    end
                )
            elif format == 'latex':
                return RawInline(
                    "latex",
                    "\SI{" + number.strip() + "}{" + unit.strip() + "}")
            else:
                return Str(number.strip() + " " + unit.strip())


if __name__ == "__main__":
    toJSONFilter(caps)
