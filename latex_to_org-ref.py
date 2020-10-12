#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Pandoc filter to convert from latex to org using org-ref

This performs he following conversions:
- ~ to \nbsp{}_pattern
- \cite{bibkey} to cite:bibkey
- \ac.*{x} to \gls.*:x
- \ref{x} to ref:x
- \eqref{x} to eqref:x.
"""

from pandocfilters import toJSONFilter, Str, RawInline, Math
import re
import sys


# Match the unicode character for NON-BREAKING-SPACE in pandoc AST
nbsp_pattern = re.compile(r'\xa0')


def replace_unit(key, value, format, meta):
    """
    Try to perform the replacements in `value` according to `pattern`.

    If nothing is replaced the this function does not return any value.

    Parameters
    ----------
    key : (string) The pandoc element type. Here we check if it is 'Str'.
    value : (string) The original text.
    format : (string) The output format of pandoc.
    meta : Not used here.
    """
    # sys.stderr.write(f"key is: {key} - value is: {value}\n")
    if key == 'Str':
        if format == 'org':
            replacement = r"\\nbsp{}"
            newValue = nbsp_pattern.sub(replacement, value)
            # sys.stderr.write(f"--- Value is {str(value)}, newValue is {str(newValue)}\n")
            if newValue != value:
                return RawInline("latex", newValue)
    elif key == 'Cite':
        if format == 'org':
            # A cite command can have several keys. The variable bibkeys here
            # will be a list with those keys
            bibkeys = [i["citationId"] for i in value[0]]
            return Str(f"cite:{','.join(bibkeys)}")
        # sys.stderr.write(f"key is: {key} - value is: {value}\n")
    elif key == 'Span':
        # This convet the usage of acronym package commands

        # sys.stderr.write(f"key is: {key} - value is: {value}\n")
        if value[0][2][0][0] == 'acronym-label':
            label = value[0][2][0][1]
            acronym_form = value[0][2][1][1]
            form_to_command = {'singular+short': 'ac', 'plural+short': 'acp',
                               'singular+full': 'acrfull', 'singular+abbrv': 'acrshort'}
            # sys.stderr.write(f"key is: {key} - value is: {value}\n")
            return Str(f"[[{form_to_command[acronym_form]}:{label}]]")
    elif key == 'Link':
        # In case the link is a reference (\ref{something} or \eqref{something})
        # replace its converted syntax from native org-mode to org-ref syntax
        if value[0][2][0][1] == 'ref':
            link_label = value[0][2][1][1].replace(":", "-")
            return Str(f"ref:{link_label}")
        elif value[0][2][0][1] == 'eqref':
            link_label = value[0][2][1][1].replace(":", "-")
            return Str(f"eqref:{link_label}")
    elif key == 'Header':
        # Replace ':' by '-' in the header label
        value[1][0] = value[1][0].replace(":", "-")
        pass


# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
if __name__ == "__main__":
    toJSONFilter(replace_unit)

    # pattern = re.compile('\xa0')
    # s = r"lala \num{20}   lele"
    # print(pattern.search(s))



    # Tip: Try the command
    # "pandoc -f latex -t native sample.tex"
    # to see pandoc's AST
