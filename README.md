
Repository containing pandoc filters that I have implemented.


## Currently implemented filters ##

### siunitx-filter.py ###

Pandoc filter to use numbers with physical units.

In markdown you should write `NUMBER{UNIT}`.
Ex: `10{ms}`, `2.6{GHz}`, etc

The filter will then separate the number and the unit. 

In latex it will be replaced with `\SI{NUMBER}{UNIT}`;

In HTML the number + unit will inside a span tag with "phy-quantity" class,
the number alone will be in a span tag with "phy-number" class and the unit
will be in a span tag with "phy-unit" tag. You can then edit your CSS as
desired to, for instance, add a small left margin to the phy-unit class.

For all the other formats `NUMBER{UNIT}` will be replaced with `NUMBER
UNIT` (just add a space).

Note that the replacements will also work inside equations, but in that
case they will not have any span tags and just typeset as regular text.

### latex_to_org-ref ###

Pandoc filter to convert from latex to org-mode using org-ref.

This performs he following conversions:
- ~ to \nbsp{}_pattern
- \cite{bibkey} to cite:bibkey
- \ac.*{x} to \gls.*:x
- \ref{x} to ref:x
- \eqref{x} to eqref:x.


## Filter Usage ##

You can apply filters in pandoc with the the `--filter` option.

As an example, if you have the `siunitx-filter.py` filter and a
`siunitx_sample.md` file in the same folder you can convert `siunitx_sample.md` using
the filter with the following command

    pandoc --filter=./siunitx-filter.py siunitx_sample.md -o siunitx_sample.html
