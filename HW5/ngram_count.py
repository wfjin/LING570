""" This python program reads a training file and outputs the ngram count for unigrams, bigrams
and trigrams of the training data """

import sys

def addebos(line_ebos):
    """ This function adds BOS and EOS to each sentence """
    new_line = ['<s>']
    new_line.extend(line_ebos)
    new_line.append('</s>')
    return new_line

if __name__ == "__main__":
    UNIGRAM = {}
    BIGRAM = {}
    TRIGRAM = {}
    with open(sys.argv[1], 'r') as training:
        for line in training:
            words = line.split()
            words = addebos(words)
            for i in range(0, len(words)):
                if words[i] in UNIGRAM:
                    UNIGRAM[words[i]] += 1
                else:
                    UNIGRAM[words[i]] = 1
                if i < len(words) - 1:
                    bi_words = words[i] + ' ' + words[i+1]
                    if bi_words in BIGRAM:
                        BIGRAM[bi_words] += 1
                    else:
                        BIGRAM[bi_words] = 1
                if i < len(words) - 2:
                    tri_words = words[i] + ' ' + words[i+1] + ' ' + words[i+2]
                    if tri_words in TRIGRAM:
                        TRIGRAM[tri_words] += 1
                    else:
                        TRIGRAM[tri_words] = 1

        SORTED_UNIGRAM = sorted(UNIGRAM.items(), key=lambda x: (x[1], x[0]), reverse=True)
        SORTED_BIGRAM = sorted(BIGRAM.items(), key=lambda x: (x[1], x[0]), reverse=True)
        SORTED_TRIGRAM = sorted(TRIGRAM.items(), key=lambda x: (x[1], x[0]), reverse=True)
    NGRAM_COUNT = open(sys.argv[2], 'w')
    for uni in SORTED_UNIGRAM:
        NGRAM_COUNT.write(str(uni[1])+'\t'+uni[0]+'\n')
    for bi in SORTED_BIGRAM:
        NGRAM_COUNT.write(str(bi[1])+'\t'+bi[0]+'\n')
    for tri in SORTED_TRIGRAM:
        NGRAM_COUNT.write(str(tri[1])+'\t'+tri[0]+'\n')
