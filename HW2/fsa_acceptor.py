import sys
import os
import string
import subprocess

def output_generator(input,sign):
    if (len(input)<12):
        output_str = input + (' '*(12-len(input))) + "=> " + sign
    else:
        output_str = input + ('\t' + "=> " + sign)
    return output_str        

if __name__ == "__main__":
    input_file = sys.argv[2]
    input_fsa = sys.argv[1]
    with open(input_file,'r') as f:
        for line in f:
            line_output = os.popen("echo '" + line +"' | carmel -sli "+input_fsa).read()
            if (line[len(line)-1] == "\n"):
                output_string = line[:len(line)-1]
            else:
                output_string = line
                
            if (line_output != ""):
                output_line = output_generator(output_string,"yes")
            else :
                output_line = output_generator(output_string,"no")
            print (output_line)
