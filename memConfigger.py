import sys

if (len(sys.argv) != 2):
    print ("Please provide an input-file.")
    print ("\"python memConfigger.py <input-file>\"")
    print(sys.argv)
    sys.exit();

inputFile = open(sys.argv[1], "r")

memSize = 0
cIndex = 0
memStruct = []
for line in inputFile.readlines():
    line = line.lstrip(' ').replace('\n', '')

    if (line == ''): continue # Skip blank lines
    if (line[0] == '#'): continue # Skip comments

    # If the line is an parser instruction
    if (line[0] == "!"):
        command = line.replace('!', '').split(' ')

        if (command[0] == "SIZE"):
            memSize = int(float(command[1]))
        elif (command[0] == "INC"):
            cIndex = cIndex + int(float(command[1]))
        else:
            print ("Command \"" + command[0] + "\" is not valid. Exiting...")
            sys.exit()

    # If the line is not an parser instruction
    else:
        expression = line.split(' ')
        elength = 0
        ename = ""
        etype = ""

        # Determine how many bytes are needed for the selected type
        if (expression[0] == "STR_ASCII"):
            elength = int(float(expression[1])) - 1
            ename = expression[2]
            etype = expression[0]
        elif (expression[0] == "LONG"):
            elength = 1
            ename = expression[1]
            etype = expression[0]
        elif (expression[0] == "INT"):
            length = 0
            ename = expression[1]
            etype = expression[0]
        else:
            print ("ERR: type \"" + etype + "\" is not valid. Exiting...")
            sys.exit()

        # Find start and stop of variable
        start = cIndex
        stop = cIndex + elength
        cIndex = stop + 1
        if (stop > memSize):
            print ("Warning: You have now used " + str(int(stop / (memSize / 100.0))) + "% of the available space, by adding \"" + ename + "\".")

        # Add var to array
        memStruct.append([
            etype,
            ename,
            elength,
            start,
            stop
        ])

# Print to human-readable file
LLongestName = 0
LLongestType = 9
LLongestStartN = len(str(memStruct[-1][2]))
LPadding = 4
for variable in memStruct:
    if (len(variable[1]) > LLongestName):
        LLongestName = len(variable[1])

with open(sys.argv[1].split('.')[0] + ".out.adoc", "w") as hOut:

    hOut.write(sys.argv[1].split('.')[0] + '\n')
    hOut.write(('-' * len(sys.argv[1].split('.')[0]) + "\n\n"))

    for variable in memStruct:
        # Name + padding
        outStr = variable[1]
        outStr = outStr + (' ' * (LLongestName - len(variable[1]) + LPadding))
        # Type + padding
        outStr = outStr + variable[0]
        outStr = outStr + (' ' * (LLongestType - len(variable[0]) + LPadding))
        # StartPos + padding
        outStr = outStr + str(variable[3])
        outStr = outStr + (' ' * (LLongestStartN - len(str(variable[3])) + LPadding))
        # EndPos
        outStr = outStr + str(variable[4])

        hOut.write(outStr + '\n')

    hOut.write("\nTYPES\n-----\n")
    hOut.write("*STR_ASCII* Hver byte er et ascii-tegn\n")
    hOut.write("*INT* en byte.\n")
    hOut.write("*LONG* to bytes, altsaa det dobbelte av en int. tallene legges sammen.\n")
    print ("Human-readable file was made : \"" + sys.argv[1].split('.')[0] + ".out.adoc\".")

# Print C++ code, this block WILL remove the first item of the list, so beware!!!
with open(sys.argv[1].split('.')[0] + ".out.cpp", "w") as cppOut:
    cppOut.write("#region GENERATED_CODE\n")
    cppOut.write("struct memoryAdress memoryAccess::getAddress(String varName) {\n")
    cppOut.write("\tmemoryAdress tmp;\n")

    specialCase = memStruct.pop(0)
    cppOut.write("\tif ((String \"" + specialCase[1] + "\" == varName)")
    cppOut.write("{tmp={" + str(specialCase[3]) + "," + str(specialCase[4]) + "};}\n")

    for variable in memStruct:
        cppOut.write("\telse if ((String) \"" + variable[1] + "\" == varName)")
        cppOut.write("{tmp={" + str(variable[3]) + "," + str(variable[4]) + "};}\n")

    cppOut.write("\treturn tmp;\n")
    cppOut.write("}\n")
    cppOut.write("#endregion")
    print ("CPP-function was made : \"" + sys.argv[1].split('.')[0] + ".out.cpp\".")
