""" This program takes an annotated training data with tag information
and returns a 2gram HMM with calculated probabilities
"""

import sys
import operator


def addebos(line_ebos):
    """ This function adds BOS and EOS to each sentence """
    new_line = ['<s>/BOS']
    new_line.extend(line_ebos)
    new_line.append('</s>/EOS')
    return new_line

def extract_tag(words):
    """ This function extracts tags and returns a sequence of tags """
    tag_list = list()
    tag_list_2gram = list()
    tag_list_3gram = list()
    word_tag_list = list()
    for word in words:
        if word == '</s>/EOS':
            word_tag_list.append(('EOS','</s>'))
            tag_list.append('EOS')
            continue
        if word == '<s>/BOS':
            word_tag_list.append(('BOS','<s>'))
            tag_list.append('BOS')
            continue
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
    for i in range(0,len(tag_list)-2):
        tag_list_3gram.append((tag_list[i],tag_list[i+1],tag_list[i+2]))
    return (tag_list, tag_list_2gram, tag_list_3gram, word_tag_list)

def tag_collection(tags, tags_2, tags_3, word_tags, word_list, tag_list):
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
    for tag in tag_list[2]:
        if tag in tags_3:
            tags_3[tag] += 1
        else:
            tags_3[tag] = 1
    for word_tag in tag_list[3]:
        if word_tag in word_tags:
            word_tags[word_tag] += 1
        else:
            word_tags[word_tag] = 1
        word_list.add(word_tag[1])
    return (tags, tags_2, word_tags)

def tags_2_possible(list_of_tags):
    tags_two = list()
    for key1 in list_of_tags:
        for key2 in list_of_tags:
            tags_two.append((key1,key2))
    return tags_two


if __name__ == "__main__":
    HMM = open(sys.argv[1], 'w')
    LAM1 = float(sys.argv[2])
    LAM2 = float(sys.argv[3])
    LAM3 = float(sys.argv[4])
    training = sys.stdin.readlines()
    with open(sys.argv[5], 'r') as unknown:
        unkown_prob = dict()
        for line in unknown:
            words = line.split()
            unkown_prob[words[0]] = float(words[1])
        tag_collect = dict()
        tag_2gram_collect = dict()
        tag_3gram_collect = dict()
        word_tag_collect = dict()
        word_list = set()
        num_tags = 0
        for line in training:
            sentence = line.split()
            sentence = addebos(sentence)
            tag_list_sum = extract_tag(sentence)
            num_tags += len(tag_list_sum[0])
            tagss = tag_collection(tag_collect, tag_2gram_collect, tag_3gram_collect, word_tag_collect, word_list, tag_list_sum)
        print_first = list()
        print_last = list()
        print_other = list()
        tagsize = len(tag_collect)
        two_tags = tags_2_possible(tag_collect)
        stateset = set()
        for tag in tag_collect:
            for tags in two_tags:
                pair = (tags[0], tags[1])
                if tags[1] == 'EOS':
                    if tag == 'EOS':
                        prob = 1
                        continue
                    else:
                        prob = 0
                        continue
                prob1 = tag_collect[tag]/num_tags
                if (tags[1],tag) in tag_2gram_collect:
                    prob2 = tag_2gram_collect[(tags[1],tag)]/tag_collect[tags[1]]
                else:
                    prob2 = 0
                if pair not in tag_2gram_collect:
                    if tag == 'BOS':
                        prob3 = 0
                    else:
                        prob3 = 1/(tagsize-1)
                else:
                    if (tags[0], tags[1], tag) in tag_3gram_collect:                    
                        prob3 = tag_3gram_collect[(tags[0], tags[1], tag)]/tag_2gram_collect[(tags[0], tags[1])]
                    else:
                        prob3 = 0
                prob = LAM3*prob3+LAM2*prob2+LAM1*prob1
                stateset.add(tags[0]+'_'+tags[1])
                stateset.add(tags[1]+'_'+tag)
                if tags[0] == 'BOS':
                    if (tags[0], tags[1], tag, prob) not in print_first:
                        print_first.append((tags[0], tags[1], tag, prob))
                elif tag == 'EOS':
                    if (tags[0], tags[1], tag, prob) not in print_last:
                        print_last.append((tags[0], tags[1], tag, prob))
                else:
                    if (tags[0], tags[1], tag, prob) not in print_other:
                        print_other.append((tags[0], tags[1], tag, prob))
        HMM.write('state_num='+str(len(stateset))+'\n')
        HMM.write('sym_num='+str(len(word_list))+'\n')
        HMM.write('init_line_num=1'+'\n')
        HMM.write('trans_line_num='+str(len(print_first)+len(print_last)+len(print_other))+'\n')
        HMM.write('emiss_line_num='+str(len(word_tag_collect)*len(tag_collect)+len(unkown_prob)*len(tag_collect))+'\n\n')
        HMM.write('\init'+'\n'+'BOS'+'\t'+'1.0\n\n\n\n')
        HMM.write('\\transitions\n')
        print_other = sorted(print_other,key=operator.itemgetter(0))
        print_first = sorted(print_first,key=operator.itemgetter(0))
        print_last = sorted(print_last,key=operator.itemgetter(0))
        probtotal = 0
        for p in (print_first+print_other+print_last):
            from_state = p[0]+'_'+p[1]
            to_state = p[1]+'_'+p[2]
            prob = p[3]
            HMM.write(from_state+'\t\t'+to_state+'\t'+'\t'+str(prob)+'\n')
        HMM.write('\n\emission\n')
        word_tag_list_sorted = sorted(word_tag_collect,key=operator.itemgetter(0))
        for word_tag in word_tag_list_sorted:
            to_state = word_tag[0]
            statelist = list()
            for from_state in tag_collect:
                state = from_state+'_'+to_state
                if state in statelist:
                    continue
                else:
                    statelist.append(state)
                symb = word_tag[1]
                if to_state in unkown_prob:
                    prob = word_tag_collect[word_tag]/tag_collect[to_state]*(1-float(unkown_prob[to_state]))
                else:
                    prob = word_tag_collect[word_tag]/tag_collect[to_state]
                HMM.write(state+'\t'+symb+'\t'+'\t'+str(prob)+'\n')                    
        for tag_unkown in unkown_prob:
            symb = '<unk>'
            prob = float(unkown_prob[tag_unkown])
            for from_state in tag_collect:
                state = from_state+'_'+tag_unkown
                HMM.write(state+'\t'+symb+'\t'+'\t'+str(prob)+'\n')
        
            