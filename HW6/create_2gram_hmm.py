""" This program takes an annotated training data with tag information
and returns a 2gram HMM with calculated probabilities
"""

import sys
import operator

def addebos(line_ebos):
    """ This function adds BOS and EOS to each sentence """
    new_line = ['<s>/BOS']
    new_line.extend(line_ebos)
    new_line.append('<e>/EOS')
    return new_line

def extract_tag(words):
    """ This function extracts tags and returns a sequence of tags """
    tag_list = list()
    tag_list_2gram = list()
    word_tag_list = list()
    for word in words:
        if '\/' not in word:
            word_split = word.split('/')
            tag_list.append(word_split[1])
            if word_split[1] == 'BOS' or word_split[1] == 'EOS':
                continue
            else:
                word_tag_list.append((word_split[1],word_split[0]))
        else:
            word_split = word.split('\/')
            tag_split = word_split[1].split('/')
            tag_list.append(tag_split[1])
            word = word_split[0]+'/'+tag_split[0]
            word_tag_list.append((tag_split[1],word))
    for i in range(0,len(tag_list)-1):
        tag_list_2gram.append((tag_list[i],tag_list[i+1]))
    return (tag_list,tag_list_2gram, word_tag_list)

def tag_collection(tags, tags_2, word_tags, word_list, tag_list):
    """ Adds the tags from tag_list to the total tag collection """
    for tag in tag_list[0]:
        if tag in tags:
            tags[tag] += 1
        else:
            tags[tag] = 1
    for tag in tag_list[1]:
        if tag in tags_2:
            tags_2[tag] += 1
        else:
            tags_2[tag] = 1
    for word_tag in tag_list[2]:
        if word_tag in word_tags:
            word_tags[word_tag] += 1
        else:
            word_tags[word_tag] = 1
        word_list.add(word_tag[1])
    return (tags, tags_2, word_tags)

if __name__ == "__main__":
    HMM = open(sys.argv[1], 'w')
    training = sys.stdin.readlines()
    tag_collect = dict()
    tag_2gram_collect = dict()
    word_tag_collect = dict()
    word_list = set()
    for line in training:
        sentence = line.split()
        sentence = addebos(sentence)
        tag_list = extract_tag(sentence)
        tag = tag_collection(tag_collect, tag_2gram_collect, word_tag_collect, word_list, tag_list)
    print_first = list()
    print_last = list()
    print_other = list()
    for tags_2gram in tag_2gram_collect:
        prob = tag_2gram_collect[tags_2gram]/tag_collect[tags_2gram[0]]
        if tags_2gram[0] == 'BOS':
            print_first.append((tags_2gram, prob))
        elif tags_2gram[1] == 'EOS':
            print_last.append((tags_2gram, prob))
        else:
            print_other.append((tags_2gram, prob))
    HMM.write('state_num='+str(len(tag_collect))+'\n')
    HMM.write('sym_num='+str(len(word_list))+'\n')
    HMM.write('init_line_num=1'+'\n')
    HMM.write('trans_line_num='+str(len(print_first)+len(print_last)+len(print_other))+'\n')
    HMM.write('emiss_line_num='+str(len(word_tag_collect))+'\n\n')
    HMM.write('\init'+'\n'+'BOS'+'\t'+'1.0\n\n\n\n')
    HMM.write('\\transitions\n')
    print_other = sorted(print_other,key=operator.itemgetter(0))    
    for p in (print_first+print_other+print_last):
        first_state = p[0][0]
        second_state = p[0][1]
        prob = p[1]
        HMM.write(first_state+'\t'+second_state+'\t'+'\t'+str(prob)+'\n')
    HMM.write('\n\emission\n')
    word_tag_list_sorted = sorted(word_tag_collect,key=operator.itemgetter(0))
    for word_tag in word_tag_list_sorted:
        state = word_tag[0]
        symb = word_tag[1]
        prob = word_tag_collect[word_tag]/tag_collect[state]
        HMM.write(state+'\t'+symb+'\t'+'\t'+str(prob)+'\n')


    
                