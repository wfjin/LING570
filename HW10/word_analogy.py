import sys
import operator
import os.path
import os
import numpy as np
import profile 
from scipy import spatial

def vectors_save(vectors, flag1):
    word_to_num = dict()
    word_vectors = list()
    num_to_word = list()
    i = 0
    for line in vectors:
        line = line.replace('\n','')
        vectors = line.split(' ')
        length = len(vectors)
        word = vectors[0]
        word_to_num[word] = i
        num_to_word.append(word)
        i += 1
        vectors.pop(0)
        vec_array = np.asarray(vectors, dtype=np.float32)
        Z_norm = np.linalg.norm(vec_array)
        if flag1 != 0:
            vec_array = vec_array/Z_norm
        word_vectors.append(vec_array)
    vec_length = len(word_vectors[0])
    for vec in word_vectors:
        if vec_length != len(vec):
            sys.exit('This is not a proper vector file')
    word_vectors.append(np.zeros(vec_length))
    return word_to_num, num_to_word, word_vectors

def input_words(input_file, word_list):
    word_list_ABC = list()
    word_list_D = list()
    word_list_ABC_words = list()
    length = len(word_list)
    for line in input_file:
        line = line.replace('\n','')
        words = line.split(' ')
        if len(words) == 4:
            try:
                A = word_list[words[0]]
            except Exception as e:
                A = length
            try:
                B = word_list[words[1]]
            except Exception as e:
                B = length
            try:
                C = word_list[words[2]]
            except Exception as e:
                C = length
            word_list_ABC.append([A,B,C])
            word_list_D.append(words[3])
            word_list_ABC_words.append([words[0],words[1],words[2]])
    return word_list_ABC, word_list_D, word_list_ABC_words

def generate_Y(word_ABC, word_vectors):
    Y_list = list()
    for ABC in word_ABC:
        A_vec = word_vectors[ABC[0]]
        B_vec = word_vectors[ABC[1]]
        C_vec = word_vectors[ABC[2]]
        Y_vec = B_vec - A_vec + C_vec
        Y_list.append(Y_vec)
    return Y_list

def process_every_file(filename, word_list, input_dir, output_dir, word_vectors, num_to_word, flag2):
    file_path = os.path.join(input_dir, filename)
    with open (file_path,'r') as input_file:
        word_ABC, word_D, word_ABC_words = input_words(input_file, word_list)
        Y_list = generate_Y(word_ABC, word_vectors)
        correct = 0
        total_num = len(Y_list)
        results = list()
        if flag2 == 0:
            euc_dist = spatial.distance.cdist(Y_list, word_vectors[:-1], 'euclidean')
            for row in euc_dist:
                results.append(np.argmin(row))
        else:
            cos_sim = spatial.distance.cdist(Y_list, word_vectors[:-1], 'cosine')
            for row in cos_sim:
                results.append(np.argmin(row))
        output_path = os.path.join(output_dir, filename)
        F = open(output_path, 'w')
        for i in range(0,len(word_ABC)):
            predict_word = num_to_word[results[i]]
            if predict_word == word_D[i]:
                correct += 1
            A = word_ABC_words[i][0]
            B = word_ABC_words[i][1]
            C = word_ABC_words[i][2]
            F.write(A+' '+B+' '+C+' ')
            F.write(predict_word+'\n')
        acc = correct/total_num*100
        sys.stdout.write(filename+':\n')
        sys.stdout.write('ACCURACY TOP1: '+str(acc)+'% ('+str(correct)+'/'+str(total_num)+')'+'\n')
    return correct, total_num

if __name__ == "__main__":
    flag1 = float(sys.argv[4])
    flag2 = float(sys.argv[5])
    input_dir = sys.argv[2]
    output_dir = sys.argv[3]
    with open(sys.argv[1],'r') as vec:
        word_list, num_to_word, word_vectors = vectors_save(vec, flag1)
        corsum = 0
        numsum = 0
    for filename in sorted(os.listdir(input_dir)):
        correct, total_num = process_every_file(filename, word_list, input_dir, output_dir, word_vectors, num_to_word, flag2)
        corsum += correct
        numsum += total_num
    total_acc = corsum/numsum*100
    sys.stdout.write('\n')
    sys.stdout.write('Total accuracy: '+str(total_acc)+'% ('+str(corsum)+'/'+str(numsum)+')'+'\n')


    

    
        
