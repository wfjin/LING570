import sys
import os

def output_generator(input,sign):
    if (len(input)<12):
        output_str = input + (' '*(12-len(input))) + "=> " + sign
    else:
        output_str = input + ('\t' + "=> " + sign)
    return output_str        

if __name__ == "__main__":
    input_file = sys.argv[2]
    input_fsa = sys.argv[1]
    output_file = sys.argv[3]
    output = open (output_file,'w')
    with open(input_file,'r') as f:
        for line in f:
            lineLetters = ''
            for letter in line:
                lineLetters = lineLetters + '\"'+letter+'\" '
            line_output = os.popen("echo '" + lineLetters +"' | carmel -sli "+input_fsa).read()
            if (line[len(line)-1] == "\n"):
                output_string = line[:len(line)-1]
            else:
                output_string = line
                
            if (line_output != ""):
                output_line = output_string + " => yes"
            else:
                output_line = output_string + " => no"
            output.write(output_line+'\n')
