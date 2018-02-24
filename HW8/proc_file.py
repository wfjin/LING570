import sys
import operator

def remove_header(inputfile):
    i = 0
    with open("input_no_header",'w') as output:
        for line in inputfile:
            if i == 0:
                if line != '\n':
                    continue
                else:
                    i = 1
                    continue
            else:
                output.write(line)
    return output

def replace_with_ws(inputfile):
    with open("input_replace_ws",'w') as output:
        for line in inputfile:
            for char in line:
                if char != ' ' and char != '\n' and char.isalpha() == False:
                    output.write(' ')
                else:
                    lowercase = char.lower()
                    output.write(lowercase)
    return output

def create_feature_vector(inputfile):
    features = dict()
    for line in inputfile:
        words = line.split()
        if len(words) == 0:
            continue
        else:
            for i in words:
                if i in features:
                    features[i] += 1
                else:
                    features[i] = 1
    sorted_feature = sorted(features.items(), key=operator.itemgetter(0))
    return sorted_feature

if __name__ == "__main__":
    output = open(sys.argv[3], 'w')
    with open(sys.argv[1],'r') as inputfile:
        input_no_header = remove_header(inputfile)
    with open("input_no_header",'r') as no_header:
        replace_ws = replace_with_ws(no_header)
    with open("input_replace_ws",'r') as ws_rep:
        feature_vec = create_feature_vector(ws_rep)
        output.write(sys.argv[1]+' ')
        output.write(sys.argv[2]+' ')
        for features in feature_vec:
            if features == feature_vec[-1]:
                output.write(features[0]+' '+str(features[1])+'\n')
            else:
                output.write(features[0]+' '+str(features[1])+' ')
        

