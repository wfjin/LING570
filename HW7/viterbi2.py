import sys
import math

def line_breakers(hmm_file):
    breakers = list()
    j = 0
    for line in hmm_file:
        j += 1
        if '\init' in line:
            breakers.append(j)
        elif '\\transition' in line:
            breakers.append(j)
        elif '\emission' in line:
            breakers.append(j)
    return breakers

def symb_state_list(hmm_file, line_breakers):
    i = 0
    j = 0
    q = 0
    init_start = line_breakers[0]
    transition_start = line_breakers[1]
    emission_start = line_breakers[2]
    statelist = dict()
    wordlist = dict()
    for line in hmm_file:
        i += 1
        if i < init_start:
            continue
        elif i > init_start and i < transition_start:
            sentence = line.split()
            if len(sentence) == 0:
                continue
            st_state = sentence[0]
            if st_state not in statelist:
                statelist[st_state] = j
                j += 1
        elif i > transition_start and i < emission_start:
            sentence = line.split()
            if len(sentence) == 0:
                continue
            from_state = sentence[0]
            to_state = sentence[1]
            if from_state not in statelist:
                statelist[from_state] = j
                j += 1
            if to_state not in statelist:
                statelist[to_state] = j
                j += 1
        elif i > emission_start:
            sentence = line.split()
            if len(sentence) == 0:
                continue
            from_state = sentence[0]
            from_id = statelist[from_state]
            symb = sentence[1]
            if symb not in wordlist:
                wordlist[symb] = q
                q += 1
    return (statelist, wordlist)
        
def index_to_state(state_list):
    index_to_state_list = dict()
    for s in state_list:
        index_to_state_list[state_list[s]] = s
    return index_to_state_list

def store_hmm(hmm_file, line_breakers, statelist, wordlist):
    i = 0
    init_start = line_breakers[0]
    transition_start = line_breakers[1]
    emission_start = line_breakers[2]
    state_num = len(statelist)
    symb_num = len(wordlist)
    j = 0
    q = 0
    start_list = []
    transitions = []
    emissions = []
    reverse_emissions = []
    for l in range(0, symb_num):
        temp1 = []
        reverse_emissions.append(temp1)
    for l in range(0, state_num):
        start_list.append(0)
    for l in range(0, state_num):
        temp1 = []
        temp2 = []
        for m in range(0, state_num):
            temp1.append(0)
        transitions.append(temp1)
        for n in range(0, symb_num):
            temp2.append(0)
        emissions.append(temp2)
    
    for line in hmm_file:
        i += 1
        if i < init_start:
            continue
        elif i > init_start and i < transition_start:
            sentence = line.split()
            if len(sentence) == 0:
                continue
            st_state = sentence[0]
            st_prob = float(sentence[1])
            st_id = statelist[st_state]
            start_list[st_id] = st_prob
            
        elif i > transition_start and i < emission_start:
            sentence = line.split()
            if len(sentence) == 0:
                continue
            from_state = sentence[0]
            to_state = sentence[1]
            from_id = statelist[from_state]
            to_id = statelist[to_state]
            prob = float(sentence[2])
            transitions[from_id][to_id] = prob         
            
        elif i > emission_start:
            sentence = line.split()
            if len(sentence) == 0:
                continue
            from_state = sentence[0]
            from_id = statelist[from_state]
            symb = sentence[1]
            symb_id = wordlist[symb]
            prob = float(sentence[2])
            emissions[from_id][symb_id] = prob
            if from_id not in reverse_emissions[symb_id]:
                reverse_emissions[symb_id].append(from_id)
    return (start_list, transitions, emissions, reverse_emissions)
    
def convert_state(state_path):
    output_string = ""
    for s in state_path:
        output_string += s
        output_string += ' '
    return output_string


if __name__ == "__main__":
    output = open(sys.argv[3], 'w')
    with open(sys.argv[1],'r') as hmm1:
        line_breakers = line_breakers(hmm1)
        init_start = line_breakers[0]
        transition_start = line_breakers[1]
        emission_start = line_breakers[2]
    with open(sys.argv[1], 'r') as hmm:
        (statelist, wordlist) = symb_state_list(hmm, line_breakers)
        index2state = index_to_state(statelist)
    with open(sys.argv[1], 'r') as hmm2:
        (start_state, transitions, emissions, reverse_emissions) = store_hmm(hmm2, line_breakers, statelist, wordlist)   
    
    with open(sys.argv[2], 'r') as test:
        for line in test:
            sentence = line.split(' ')
            if (len(sentence) == 0 or len(sentence) == 1):
                continue
            sentence.insert(0, '<s>')
            if '\n' in sentence[len(sentence)-1]:
                sentence[len(sentence)-1] = sentence[len(sentence)-1].replace('\n','')
            sentence_list = []
            for word in sentence:
                if word in wordlist:
                    sentence_list.append(wordlist[word])
                else:
                    sentence_list.append(wordlist['<unk>'])
            V = []
            state_num = len(statelist)
            for i in range(0, len(sentence)):
                temp = []
                for l in range(0, state_num):
                    temp.append(0)
                V.append(temp)
            path = {}         
            for i in range(0,state_num):
                symb_id = sentence_list[0]
                V[0][i] = start_state[i] * emissions[i][symb_id]
                path[i] = [i]
            for i in range(1, len(sentence)):
                V.append({})
                newpath = {}
                symb_id = sentence_list[i]
                for s in range(0,len(reverse_emissions[symb_id])):
                    prev_id = sentence_list[i-1]
                    prev_list = reverse_emissions[prev_id]                 
                    if emissions[reverse_emissions[symb_id][s]][symb_id] == 0:
                        V[i][reverse_emissions[symb_id][s]] = 0
                        newpath[reverse_emissions[symb_id][s]] = path[reverse_emissions[symb_id][s]]+[reverse_emissions[symb_id][s]]
                        continue
                    list_of_pairs = []
                    for x in range(0, len(prev_list)):
                        if transitions[prev_list[x]][reverse_emissions[symb_id][s]] == 0 or V[i-1][prev_list[x]] == 0:
                            continue
                        else:
                            newprob = V[i-1][prev_list[x]] * transitions[prev_list[x]][reverse_emissions[symb_id][s]] * emissions[reverse_emissions[symb_id][s]][symb_id]
                            list_of_pairs.append((newprob, prev_list[x]))
                    if (len(list_of_pairs) == 0):
                        newpath[reverse_emissions[symb_id][s]] = path[prev_list[x]]+[reverse_emissions[symb_id][s]]
                        continue
                    else:
                        (prob,state) = max(list_of_pairs, key=lambda x:x[0])
                        V[i][reverse_emissions[symb_id][s]] = prob
                        newpath[reverse_emissions[symb_id][s]] = path[state]+[reverse_emissions[symb_id][s]]
                path = newpath
            (prob, state) = max([(V[len(sentence)-1][y], y) for y in range(0,state_num)])
            pathstring = []
            for s in path[state]:
                pathstring.append(index2state[s])
            output.write(convert_state(sentence[1:])+'=> '+convert_state(pathstring)+str(math.log10(prob))+'\n')
