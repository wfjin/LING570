import operator
import sys

def initialize_dict(input,voc):
    with open(input,'r') as f:
        for line in f:
            for word in line.split():
                voc[word] = 0

def split_dict(input,voc):
    with open(input,'r') as f:
        for line in f:
            for word in line.split():
                voc[word] += 1

if __name__ == "__main__":
    voc_list = dict();
    filename = sys.argv[1]
    initialize_dict(filename,voc_list)
    split_dict(filename,voc_list)
    sorted_voc = sorted(voc_list.items(), key=operator.itemgetter(1), reverse=True)
    for x in sorted_voc:
        print (x[0], end="")
        if len(x[0])<8:
            print(' '*(8-len(x[0])), end="")
        else:
            print ('\t', end="")
        print (x[1])
