# memConfigger
This is a simple python-script that takes a simple file with variable-names and types, and turns it into a cpp-lookup-function. I wrote it to simplify allocation of space on EEPROMS, meaning i don't have to do any math. I just have to copy-paste the function. This is probably not the best way to to it, but it works just fine.

I Might add the CPP-class that i put the resulting function into when i get time to turn it into a skeleton, and make som docs on it.

## Use
You need python installed, i believe 2.7 is what i have on my computer. Altough i don't see why it wouldn't work with Python 3 as well. I think the code is compiant. Start it with
```
python memConfigger.py <input-file>
```
If the input-file exists and have the proper data, it will produce two files. Both with the same name (Except last .\*), ending with `.out.cpp` and `.out.adoc`.

`.cpp` is the generated function, and `.adoc` is a more human-friendly lookup-table.

## Input-file
This should be a flat-file consisting of commands, one for each line. Lines that are blank, or are starting with a `#` is ignored.

If the line starts with a `!`, the following should be one of the following:
- `SIZE <INT>` This sets the max size of the EEPROM, it doesn't actually affect the execution. If you set it in the top of you file however, it will keep track of the available space on your PROM. `Defaults to 0`.
- `INC <INT>` This will push the integer forward. Making some space on you PROM, this could be usefull if you plan to reserve some space at a spesific location for later updates, that shouldn't affect the current user-data.

If the line does not start with an exlamation mark, we are assuming the first word is an type. At the moment there are only three possible types. The list below starts with how a line should look, for it to be interpereted correctly:
- `STR_ASCII <length> <variable_name>` This is just that, each byte will be an ascii character.
- `LONG <variable_name>` This is two bytes, usually you would sum them to get their value.
- `INT <variable_name>` This is just one byte.

== Example-file
```
# We are setting the size, so the parser can notify us if and when we exceed it
!SIZE 124

# Just setting some vars
STR_ASCII 10 f_name
STR_ASCII 10 l_name
INT age

# Incrementing our index by 50
!INC 50

# Setting som more vars
LONG XP
STR_ASCII 20 some_more_info
INT Another_int
```
