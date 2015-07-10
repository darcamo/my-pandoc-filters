
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

For all the other formats `NUMBER{UNIT}` will be replaced with `NUMBER UNIT`.


## Filter Usage ##

You can apply filters in pandoc with the the `--filter` option.

As an example, if you have the `siunitx-filter.py` filter and a
`siunitx_sample.md` file in the same folder you can convert `siunitx_sample.md` using
the filter with the following command

    pandoc --filter=./siunitx-filter.py siunitx_sample.md -o siunitx_sample.html
