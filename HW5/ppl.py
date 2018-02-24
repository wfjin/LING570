""" This python program reads a language model file, 3 lamda constants, and a test data
to output the perpelxity and probability for each sentance in the test data
respectively using the required format """

import sys
import math

def addebos(line_ebos):
    """ This function adds BOS and EOS to each sentence """
    new_line = ['<s>']
    new_line.extend(line_ebos)
    new_line.append('</s>')
    return new_line

def processlm(input_lm):
    """ given an input lm, store the corresponding probability and log into a dictionary """
    lmodel = {}
    for line_1 in input_lm:
        split_line = line_1.split(' ')
        if split_line[0].isdigit() is False:
            continue
        else:
            if (len(split_line)) == 4:
                word_1 = split_line[3][:-1]
                lmodel[word_1] = (float(split_line[1]), float(split_line[2]))
            if (len(split_line)) == 5:
                word_1 = split_line[3]+' '+split_line[4][:-1]
                lmodel[word_1] = (float(split_line[1]), float(split_line[2]))
            if (len(split_line)) == 6:
                word_1 = split_line[3]+' '+split_line[4]+' '+split_line[5][:-1]
                lmodel[word_1] = (float(split_line[1]), float(split_line[2]))
    return lmodel

def calcprob(word1, word2, word3, lmodel, lam1, lam2, lam3):
    """ given a language model and three words, calculate the probability """
    tri_words = word3+' '+word2+' '+word1
    bi_words = word2+' '+word1
    if tri_words in lmodel:
        prob1 = lam3*lmodel[tri_words][0]+lam2*lmodel[bi_words][0]+lam1*lmodel[word1][0]
        checker = True
    else:
        if bi_words in lmodel:
            prob1 = lam2*lmodel[bi_words][0]+lam1*lmodel[word1][0]
            checker = False
        else:
            prob1 = lam1*lmodel[word1][0]
            checker = False
    return (prob1, checker)

if __name__ == "__main__":
    PPL = open(sys.argv[6], 'w')
    PPL.write('\n')
    LAM1 = float(sys.argv[2])
    LAM2 = float(sys.argv[3])
    LAM3 = float(sys.argv[4])
    with open(sys.argv[1], 'r') as lm:
        LM_DICT = processlm(lm)
    with open(sys.argv[5], 'r') as test:
        SUM_FILE = 0
        WORD_NUM_FILE = 0
        OOV_NUM_FILE = 0
        NUM = 1
        for line in test:
            oov_num_sent = 0
            words = line.split()
            words = addebos(words)
            word_num_sent = len(words)-2
            sum_sent = 0
            WORD_NUM_FILE += word_num_sent
            PPL.write('Sent #'+str(NUM)+':')
            for word in words:
                PPL.write(' '+word)
            PPL.write('\n')
            COUNT = 0
            for word in words:
                if COUNT == 0:
                    COUNT += 1
                    continue
                elif COUNT == 1:
                    if word not in LM_DICT:
                        PPL.write(str(COUNT)+': lg P('+word+' | <s>) = -inf (unknown word)\n')
                        oov_num_sent += 1
                    else:
                        if ('<s> '+word) not in LM_DICT:
                            prob = math.log10(LAM1*LM_DICT[word][0])
                            sum_sent += prob
                            PPL.write(str(COUNT)+': lg P('+word+' | <s>) = '+str(prob)+' (unseen ngrams)\n')
                        else:
                            prob = LAM2*LM_DICT['<s> '+word][0]+LAM1*LM_DICT[word][0]
                            prob = math.log10(prob)
                            sum_sent += prob
                            PPL.write(str(COUNT)+': lg P('+word+' | <s>) = '+str(prob)+'\n')
                else:
                    if word not in LM_DICT:
                        PPL.write(str(COUNT)+': lg P('+word+' | '+words[COUNT-2]+' '+words[COUNT-1]+') = -inf (unknown word)\n')
                        oov_num_sent += 1
                    else:
                        pair = calcprob(word, words[COUNT-1], words[COUNT-2], LM_DICT, LAM1, LAM2, LAM3)
                        if pair[1]:
                            prob = math.log10(pair[0])
                            sum_sent += prob
                            PPL.write(str(COUNT)+': lg P('+word+' | '+words[COUNT-2]+' '+words[COUNT-1]+') = '+str(prob)+'\n')
                        else:
                            prob = math.log10(pair[0])
                            sum_sent += prob
                            PPL.write(str(COUNT)+': lg P('+word+' | '+words[COUNT-2]+' '+words[COUNT-1]+') = '+str(prob)+' (unseen ngrams)\n')
                COUNT += 1
            PPL.write('1 sentence, '+str(COUNT-2)+' words, '+str(oov_num_sent)+' OOVs\n')
            cnt = COUNT - 1 - oov_num_sent
            SUM_FILE += sum_sent
            OOV_NUM_FILE += oov_num_sent
            PPL.write('lgprob='+str(sum_sent)+' ppl='+str(math.pow(10, -sum_sent/cnt)))
            PPL.write('\n\n\n\n')
            NUM += 1
        CNT_FILE = NUM+WORD_NUM_FILE-OOV_NUM_FILE
        PPL.write('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n')
        PPL.write('sent_num='+str(NUM-1)+' word_num='+str(WORD_NUM_FILE)+' oov_num='+str(OOV_NUM_FILE)+'\n')
        PPL.write('lgprob='+str(SUM_FILE)+' ave_lgprob='+str(SUM_FILE/CNT_FILE)+' ppl='+str(math.pow(10,-SUM_FILE/CNT_FILE))+'\n')

