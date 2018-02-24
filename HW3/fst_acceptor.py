import sys
import os
import string
import subprocess
from decimal import Decimal

def output_generator(input,sign):
    if (len(input)<12):
        output_str = input + (' '*(12-len(input))) + "=> " + sign
    else:
        output_str = input + ('\t' + "=> " + sign)
    return output_str

def fsa_line(num,sym):
    num_str = str(num)
    num1_str = str(num+1)
    return "(" + num_str + " (" + num1_str + " " + sym + "))\n"

if __name__ == "__main__":
    input_string = sys.argv[2]
    fst = sys.argv[1]
    with open(input_string,'r') as f:
        for line in f:
            if (line[len(line)-1] == "\n"):
                output_string = line[:len(line)-1]
            else:
                output_string = line
            fsa = open('fsa_output','w')
            words = line.split()
            fsa_length = len(words)
            fsa.write(str(fsa_length)+'\n')
            for i in range(0,fsa_length):
                fsa.write(fsa_line(i,words[i]))
            fsa.close()
            line_output = os.popen("carmel -OEk 1 "+"fsa_output "+fst).read()
            if (line_output[0] == '0'):
                output_line = output_generator(output_string,"*none* 0")
            else:
                new_line = line_output.strip()
                new_line = line_output.split()
                newnew_line = ""
                for i in range(0,len(new_line)-1):
                    newnew_line = newnew_line + new_line[i] + " "
                prob = "{:.3e}".format(Decimal(new_line[len(new_line)-1]))
                newnew_line = newnew_line + str(prob)
                output_line = output_generator(output_string, newnew_line)
            print (output_line)
