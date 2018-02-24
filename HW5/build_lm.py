""" This python program reads a ngram counting file and outputs a language model in APRA format """

import sys
import math
import operator

def unigram(input_ngram):
    """ extract the unigram from input ngram """
    uni = {}
    count = 0
    for line in input_ngram:
        split_line = line.split('\t')
        count = len(split_line[1].split(' '))
        if count == 1:
            uni[split_line[1][0:len(split_line[1])-1]] = int(split_line[0])
    return uni

def bigram(input_ngram):
    """ extract the unigram from input ngram """
    bid = {}
    count = 0
    for line in input_ngram:
        split_line = line.split('\t')
        count = len(split_line[1].split(' '))
        if count == 2:
            bid[split_line[1][0:len(split_line[1])-1]] = int(split_line[0])
    return bid

def trigram(input_ngram):
    """ extract the trigram from input ngram """
    tri = {}
    count = 0
    for line in input_ngram:
        split_line = line.split('\t')
        count = len(split_line[1].split(' '))
        if count == 3:
            tri[split_line[1][0:len(split_line[1])-1]] = int(split_line[0])
    return tri


def countngram(input_ngram):
    """ count the number of types and tokens in the input ngram file """
    num_type = 0
    num_token = 0
    for key_1 in input_ngram:
        num_type += 1
        num_token += input_ngram[key_1]
    return (num_type, num_token)

if __name__ == "__main__":
    with open(sys.argv[1], 'r') as ngram:
        UNIGRAM = unigram(ngram)
    with open(sys.argv[1], 'r') as ngram:
        BIGRAM = bigram(ngram)
    with open(sys.argv[1], 'r') as ngram:
        TRIGRAM = trigram(ngram)
    UNI_COUNT = countngram(UNIGRAM)
    BI_COUNT = countngram(BIGRAM)
    TRI_COUNT = countngram(TRIGRAM)
    LM_MODEL = open(sys.argv[2], 'w')
    LM_MODEL.write('\\data\\'+'\n')
    LM_MODEL.write('ngram 1: type='+str(UNI_COUNT[0])+' token='+str(UNI_COUNT[1])+'\n')
    LM_MODEL.write('ngram 2: type='+str(BI_COUNT[0])+' token='+str(BI_COUNT[1])+'\n')
    LM_MODEL.write('ngram 3: type='+str(TRI_COUNT[0])+' token='+str(TRI_COUNT[1])+'\n\n\\1-grams:\n')
    UNIGRAM_SORTED = sorted(UNIGRAM.items(), key=operator.itemgetter(1), reverse=True)
    BIGRAM_SORTED = sorted(BIGRAM.items(), key=operator.itemgetter(1), reverse=True)
    TRIGRAM_SORTED = sorted(TRIGRAM.items(), key=operator.itemgetter(1), reverse=True)
    for key in UNIGRAM_SORTED:
        occurrence = key[1]
        prob = occurrence/UNI_COUNT[1]
        log = math.log10(prob)
        LM_MODEL.write(str(occurrence)+' '+str(prob)+' '+str(log)+' '+key[0]+'\n')
    LM_MODEL.write('\n\\2-grams:\n')
    for key in BIGRAM_SORTED:
        occurrence = key[1]
        key_split = key[0].split(' ')
        occurenct_uni = UNIGRAM[key_split[0]]
        prob = occurrence/occurenct_uni
        log = math.log10(prob)
        LM_MODEL.write(str(occurrence)+' '+str(prob)+' '+str(log)+' '+key[0]+'\n')
    LM_MODEL.write('\n\\3-grams:\n')
    for key in TRIGRAM_SORTED:
        occurrence = key[1]
        key_split = key[0].split(' ')
        bi_word = key_split[0] + ' ' + key_split[1]
        occurenct_bi = BIGRAM[bi_word]
        prob = occurrence/occurenct_bi
        log = math.log10(prob)
        LM_MODEL.write(str(occurrence)+' '+str(prob)+' '+str(log)+' '+key[0]+'\n')
    LM_MODEL.write('\n\\end\\\n')
    