

# Test 10{ms} in a header #

Some text 2.4{GHz} is the frequency value.

What about units in a list

- 100{Km/h}
- 9.81{m/s^2}

Now some things that should not be replaced.

- .{hh}
- .,'{gg}
- lala{kg}
- 127.0.0.0{IP}

Note that the above value with an IP address matched the ending "`0.0{IP}`",
but for now we are not treating this corner case.

What about a table?

| Name           | Value               |
|----------------+---------------------|
| gravity        | 9.81{m/2^2}         |
| speed of light | 299792458.00{m/s}   |
| electron mass  | 9.10938291e-31{kg}  |


And if we have parenthesis such as (1.3{ms}).

What about an ending punctuation such as 23{m/s^2}.

Note that the ending "." in the previous phrase should be present.
