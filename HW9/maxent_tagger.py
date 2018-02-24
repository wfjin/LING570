import sys
import operator
import os.path
import os

def split_word_tag(wordtag):
    if len(wordtag) <= 1:
        return
    if '\/' in wordtag:
        split1 = wordtag.split('\/')
        word1 = split1[0]
        split2 = split1[1].split('/')
        word2 = split2[0]
        tag = split2[1]
        word = word1+'\/'+word2
    else:
        word_tag_split = wordtag.split('/')
        word = word_tag_split[0]
        tag = word_tag_split[1].replace("\n",'')
    return (word,tag)


def checknumber(inputstr):
    return any(char.isdigit() for char in inputstr)

def checkupper(inputstr):
    return any(char.isupper() for char in inputstr)

def checkhyphen(inputstr):
    return any(char=='-' for char in inputstr)

def add_feature(feature_list, feature):
    if feature not in feature_list:
        feature_list.append(feature)

def create_feature_sent_2(sentence, word_list, rare_thres):
    word_list_sent = ['BOS','BOS']
    tag_list_sent = ['BOS','BOS']
    sum_features = []
    for word_tag_pair in sentence:
        (word,tag) = split_word_tag(word_tag_pair)
        word_list_sent.append(word)
        tag_list_sent.append(tag)
    word_list_sent[-1] = word_list_sent[-1].replace('\n','')
    tag_list_sent[-1] = tag_list_sent[-1].replace('\n','')
    word_list_sent.append('EOS')
    word_list_sent.append('EOS')
    tag_list_sent.append('EOS')
    tag_list_sent.append('EOS')
    for i in range(2,len(word_list_sent)-2):
        feature_list_sent = []
        add_feature(feature_list_sent, 'prevW='+word_list_sent[i-1])
        add_feature(feature_list_sent, 'prev2W='+word_list_sent[i-2])
        add_feature(feature_list_sent, 'nextW='+word_list_sent[i+1])
        add_feature(feature_list_sent, 'next2W='+word_list_sent[i+2])
        add_feature(feature_list_sent, 'prevT='+tag_list_sent[i-1])
        add_feature(feature_list_sent, 'prevTwoTags='+tag_list_sent[i-2]+'+'+tag_list_sent[i-1])
        if word_list[word_list_sent[i]] >= int(rare_thres):
            feature_list_sent.insert(0, 'curW='+word_list_sent[i])
        else:
            add_feature(feature_list_sent, 'containNum')
            add_feature(feature_list_sent, 'containUC')
            add_feature(feature_list_sent, 'containHyp')
            if (checknumber(word_list_sent[i])):
                feature_list_sent.append('containNum 1')
            if (checkupper(word_list_sent[i])):
                feature_list_sent.append('containUC 1')
            if (checkhyphen(word_list_sent[i])):
                feature_list_sent.append('containHyp 1')
            add_feature(feature_list_sent, 'pref='+word_list_sent[i][0])
            if len(word_list_sent[i]) >= 2:
                add_feature(feature_list_sent, 'pref='+word_list_sent[i][0:2])
                if len(word_list_sent) >= 3:
                    add_feature(feature_list_sent, 'pref='+word_list_sent[i][0:3])
                    if len(word_list_sent[i]) >= 4:
                        add_feature(feature_list_sent, 'pref='+word_list_sent[i][0:4])
            add_feature(feature_list_sent, 'suf='+word_list_sent[i][-1])
            if len(word_list_sent[i]) >= 2:
                add_feature(feature_list_sent, 'suf='+word_list_sent[i][-2:])
                if len(word_list_sent) >= 3:
                    add_feature(feature_list_sent, 'suf='+word_list_sent[i][-3:])
                    if len(word_list_sent[i]) >= 4:
                        add_feature(feature_list_sent, 'suf='+word_list_sent[i][-4:])
        sum_features.append(feature_list_sent)
    return (word_list_sent, tag_list_sent, sum_features)

def create_feature_sent(sentence, word_list, feature_list, rare_thres):
    tuple = create_feature_sent_2(sentence, word_list, rare_thres)
    for feature_list_sent in tuple[2]:
        for feature in feature_list_sent:
            if feature == 'containNum 1' or feature == 'containUC 1' or feature == 'containHyp 1':
                continue
            if feature in feature_list:
                feature_list[feature] += 1
            else:
                feature_list[feature] = 1

def create_feature_list(input_file, word_list, rare_thres):
    feature_list = dict()
    for line in input_file:
        sentence = line.split(' ')
        create_feature_sent(sentence, word_list, feature_list, rare_thres)
    sorted_feature_freq = sorted(feature_list.items(), key=operator.itemgetter(1), reverse=True)
    save_path = sys.argv[5]
    output_file = os.path.join(save_path, "init_feats")
    output = open(output_file, 'w')
    for word in sorted_feature_freq:
        line = ""
        line = str(word[0]) + " " + str(word[1]) + "\n"
        output.write(line)
    return feature_list

def count_word(input_file):
    word_freq = count_word_2(input_file)
    sorted_word_freq = sorted(word_freq.items(), key=operator.itemgetter(1), reverse=True)
    save_path = sys.argv[5]
    output_file = os.path.join(save_path, "train_voc")
    output = open(output_file, 'w')
    for word in sorted_word_freq:
        line = ""
        line = str(word[0]) + "\t" + str(word[1]) + "\n"
        output.write(line)
    return word_freq

def count_word_2(input_file):
    word_freq = dict()
    for line in input_file:
        if len(line) == 0:
            continue
        else:
            word_tag_pairs = line.split(' ')
            for word_tag_pair in word_tag_pairs:
                (word,tag) = split_word_tag(word_tag_pair)
                if word in word_freq:
                    word_freq[word] += 1
                else:
                    word_freq[word] = 1
    return word_freq

def remove_low_features(feature_list, feat_thres):
    kept_feature_list = dict()
    remove_feature_list = []
    for feature in feature_list:
        if feature[0:4] == 'curW':
            kept_feature_list[feature] = feature_list[feature]
            continue
        if feature_list[feature] < int(feat_thres):
            remove_feature_list.append(feature)
            continue
        else:
            kept_feature_list[feature] = feature_list[feature]
    sorted_feature_freq = sorted(kept_feature_list.items(), key=operator.itemgetter(1), reverse=True)
    save_path = sys.argv[5]
    output_file = os.path.join(save_path, "kept_feats")
    output = open(output_file, 'w')
    for word in sorted_feature_freq:
        line = ""
        line = str(word[0]) + " " + str(word[1]) + "\n"
        output.write(line)
    return remove_feature_list

def process_every_sentence(line, num, word_list, rare_thres, remove_feature_list, output):
    i = 0
    sentence = line.split(' ')
    tuple = create_feature_sent_2(sentence, word_list, rare_thres)  
    word_list = tuple[0]
    tag_list = tuple[1]
    feature_list = tuple[2]
    for feature_word in feature_list:
        if word_list[i+2] == ',':
            word_list[i+2] = 'comma'
        if tag_list[i+2] == ',':
            tag_list[i+2] = 'comma'
        output_line = str(num)+'-'+str(i)+'-'+word_list[i+2]+' '+tag_list[i+2]
        for feature in feature_word:
            if feature == 'containNum' or feature == 'containUC' or feature == 'containHyp':
                continue
            if feature not in remove_feature_list:
                feature = feature.replace(',','comma')
                if feature == 'containNum 1' or feature == 'containUC 1' or feature == 'containHyp 1':
                    output_line += ' '+feature
                else:
                    output_line += ' '+feature + ' 1'
            else:
                continue
        output_line += '\n'
        output.write(output_line)
        i += 1
    

def process_file(inputfile, word_list, rare_thres, remove_feature_list):
    save_path = sys.argv[5]
    output_file = os.path.join(save_path, "final_train.vectors.txt")
    output = open(output_file, 'w')
    j = 1
    for line in inputfile:
        process_every_sentence(line, j, word_list, rare_thres, remove_feature_list, output)
        j += 1

def process_file_test(inputfile, word_list, rare_thres, remove_feature_list):
    save_path = sys.argv[5]
    output_file = os.path.join(save_path, "final_test.vectors.txt")
    output = open(output_file, 'w')
    j = 1
    for line in inputfile:
        process_every_sentence(line, j, word_list, rare_thres, remove_feature_list, output)
        j += 1

if __name__ == "__main__":
    rare_thres = sys.argv[3]
    feat_thres =sys.argv[4]
    with open(sys.argv[1],'r') as inputfile:
        word_list = count_word(inputfile)
        word_list['comma'] = word_list[',']
    with open(sys.argv[1],'r') as inputfile:
        feature_list = create_feature_list(inputfile, word_list, rare_thres)
        remove_feature_list = remove_low_features(feature_list, feat_thres)
    with open(sys.argv[1],'r') as inputfile:
        process_file(inputfile, word_list, rare_thres, remove_feature_list)
    
    with open(sys.argv[2],'r') as testfile:
        word_list_test = count_word_2(testfile)
        word_list_test['comma'] = word_list_test[',']
    with open(sys.argv[2],'r') as testfile:
        process_file_test(testfile, word_list_test, rare_thres, remove_feature_list)
    save_path = sys.argv[5]
    train_vec = os.path.join(save_path, "final_train.vectors.txt")
    train_vec_out = os.path.join(save_path, "final_train.vectors")
    test_vec = os.path.join(save_path, "final_test.vectors.txt")
    test_vec_out = os.path.join(save_path, "final_test.vectors")
    me_model = os.path.join(save_path, "me_model")
    me_model_stdout = os.path.join(save_path, "me_model.stdout")
    me_model_stderr = os.path.join(save_path, "me_model.stderr")
    sys_out = os.path.join(save_path, "sys_out")
    os.system("mallet import-file --input "+train_vec+" --output "+train_vec_out)
    os.system("mallet import-file --input "+test_vec+" --output "+test_vec_out+" --use-pipe-from "+train_vec_out)
    os.system("mallet train-classifier --trainer MaxEnt --input "+train_vec_out+" --output-classifier "+me_model+" 1>"+me_model_stdout+" 2>"+me_model_stderr)
    os.system("mallet classify-file --input "+test_vec+" --classifier "+me_model+" --output "+sys_out)
    os.system("vectors2classify --training-file "+train_vec_out+" --testing-file "+test_vec_out+" --trainer MaxEnt --report test:raw test:accuracy test:confusion train:confusion train:accuracy > acc.stdout 2>acc.stdout")
    #os.system("vectors2classify --training-file "+train_vec_out+" --testing-file "+test_vec_out+" --trainer MaxEnt --ouput-classifier "+me_model+" --output "+sys_out+" > "+me_model_stdout+" 2> "+me_model_stderr)

    
        