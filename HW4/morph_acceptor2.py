import sys
import os
import string

def fsa_line(num,sym):
    num_str = str(num)
    num1_str = str(num+1)
    return "(" + num_str + " (" + num1_str + " \"" + sym + "\"))\n"

if __name__ == "__main__":
    input_file = sys.argv[2]
    fst = sys.argv[1]
    output_file = sys.argv[3]
    output = open(output_file,'w')
    with open(input_file, 'r') as f:
        for line in f:
            if (line[len(line)-1] == "\n"):
                output_string = line[:len(line)-1]
            else:
                output_string = line
            fsa = open('fsa_output', 'w')
            words = line.split()
            fsa_length = len(words[0])
            fsa.write(str(fsa_length)+'\n')
            for i in range(0,fsa_length):
                fsa.write(fsa_line(i,words[0][i]))
            fsa.close()
            
            line_output = os.popen("carmel -OEk 1 "+"fsa_output "+fst).read()
            if (line_output[0] == '0'):
                output_line = output_string+" => *none*"
            else:
                new_line = line_output.strip()
                splitting = new_line.split()
                morph_label = ""
                i = 0
                while i < len(splitting)-1:
                    morph_label = morph_label + splitting[i][1:] + "/" + splitting[i+1][0:len(splitting[i+1])-1]+" "
                    i += 2
                output_line = output_string+" => "+morph_label
            output.write(output_line+'\n')
