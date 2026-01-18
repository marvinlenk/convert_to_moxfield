import argparse

# parse argument, first argument must be input file
parser = argparse.ArgumentParser()
parser.add_argument('inputfile_path', help="Input file path")
args = parser.parse_args()

# store input file path, find ending and replace it accordingly for the outputfile path
inputfile_path = args.inputfile_path
inputfile_path_dotposition = inputfile_path.rfind(".")
outputfile_path = inputfile_path[0:inputfile_path_dotposition] + "_moxfield.txt"

with open (outputfile_path, 'w') as outputfile:
    with open(inputfile_path, 'r') as inputfile:
        inputlines = inputfile.readlines()
        currenttag = ""
        for line in inputlines:
            # skip blank lines
            if not line.strip():
                continue

            # check comment lines with leading "//"
            if line[0:2] == "//":
                # skip NAME comment line
                if line[2:7] == "NAME:":
                    continue
                if "Sideboard" in line:
                    outputfile.write("\nSideboard:\n")
                    currenttag = ""
                    continue
                if "Maybeboard" in line:
                    outputfile.write("\nConsidering:\n")
                    currenttag = ""
                    continue
                # update tag to current comment
                currenttag = line[2:].rstrip()
                #print("Changed current tag to #" + currenttag)
                continue
            
            # find first blank to find end of card count
            firstblank = line.find(" ")
            # store count
            card_count = line[0:firstblank]
            linerest = line[firstblank:].lstrip()

            card_set_code = ""
            card_collector_number = ""

            # check if set and/or collector number is given
            if linerest[0] == "[":
                endofbracket = linerest.find("]")
                bracket_contents = linerest[1:endofbracket]

                card_set_code = bracket_contents[0:3]
                # check if collector number is given
                if "#" in bracket_contents:
                    card_collector_number = bracket_contents[4:]
                linerest = linerest[endofbracket+1:].lstrip()

            # check if card comment is given, discard if found
            if "#" in linerest:
                commentposition = linerest.find("#")
                card_name = linerest[0:commentposition].rstrip()
            else:
                card_name = linerest.rstrip()
            

            # combine everything into new line in output
            outputfile.write(card_count + " " + card_name)
            if card_set_code:
                outputfile.write(" (" + card_set_code + ")")
            if card_collector_number:
                outputfile.write(" " + card_collector_number)
            if currenttag:
                outputfile.write(" #" + currenttag)
            outputfile.write("\n")
