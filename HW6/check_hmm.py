import sys
from decimal import Decimal as D

def ASCII(s):
    x = 0
    for i in range(len(s)):
        x += ord(s[i])*2**(8 * (len(s) - i - 1))
    return x

def get_nums(hmm):
    i = 1
    for line in hmm:
        if i == 1:
            state_num = int(line.split('=')[1])
        elif i == 2:
            sym_num = int(line.split('=')[1])
        elif i == 3:
            init_line_num = int(line.split('=')[1])
        elif i == 4:
            trans_line_num = int(line.split('=')[1])
        elif i == 5:
            emiss_line_num = int(line.split('=')[1])
        else:
            break
        i += 1
    return (state_num, sym_num, init_line_num, trans_line_num, emiss_line_num)

def add_probs(transition_lines):
    sum_prob = dict()
    for from_state in transition_lines:
        sum_from = 0
        for pair in transition_lines[from_state]:
            sum_from += pair[1]
        sum_prob[from_state] = sum_from
    return sum_prob

def line_breakers(hmm_file):
    breakers = list()
    j = 0
    for line in hmm_file:
        j += 1
        if '\init' in line:
            breakers.append(j)
        elif '\\transition' in line:
            breakers.append(j)
        elif 'emission' in line:
            breakers.append(j)
    return breakers

if __name__ == "__main__":
    with open(sys.argv[1],'r') as hmm1:
        line_breakers = line_breakers(hmm1)
        init_start = line_breakers[0]
        transition_start = line_breakers[1]
        emission_start = line_breakers[2]
    with open(sys.argv[1], 'r') as hmm2:
        nums_tuple = get_nums(hmm2)
    with open(sys.argv[1], 'r') as hmm:
        i = 0
        transitions = dict()
        start_state = dict()
        emissions = dict()
        taglist = set()
        wordlist = set()
        statelist = set()
        num_transitions = 0
        num_emissions = 0        
        for line in hmm:
            i += 1
            if i < init_start:
                continue
            elif i > init_start and i < transition_start:
                sentence = line.split()
                if len(sentence) == 0:
                    continue
                st_state = sentence[0]
                st_prob = float(sentence[1])
                start_state[st_state]=st_prob
                taglist.add(st_state)
            elif i > transition_start and i < emission_start:
                sentence = line.split()
                if len(sentence) == 0:
                    continue
                from_state = sentence[0]
                to_state = sentence[1]
                statelist.add(from_state)
                statelist.add(to_state)
                prob = D(sentence[2])
                states_from = from_state.split('_')
                states_to = to_state.split('_')
                if len(states_from) == 1:
                    taglist.add(states_from[0])
                else:
                    taglist.add(states_from[0])
                    taglist.add(states_from[1])
                if len(states_to) == 1:
                    taglist.add(states_to[0])
                else:
                    taglist.add(states_to[0])
                    taglist.add(states_to[1])
                if from_state in transitions:
                    transitions[from_state].append((to_state, prob))
                else:
                    temp = list()
                    temp.append((to_state, prob))
                    transitions[from_state] = temp
                num_transitions += 1
            elif i > emission_start:
                sentence = line.split()
                if len(sentence) == 0:
                    continue
                from_state = sentence[0]
                symb = sentence[1]
                states_from = from_state.split('_')
                if len(states_from) == 1:
                    taglist.add(states_from[0])
                else:
                    taglist.add(states_from[0])
                    taglist.add(states_from[1])
                wordlist.add(symb)
                prob = D(sentence[2])
                if from_state in emissions:
                    emissions[from_state].append((symb, prob))
                else:
                    temp = list()
                    temp.append((symb, prob))
                    emissions[from_state] = temp
                num_emissions += 1
        if '<unk>' in wordlist:
            wordlist.remove('<unk>')
        if len(statelist) != nums_tuple[0]:
             sys.stdout.write('warning: different numbers of state_num: claimed='+str(nums_tuple[0])+', real='+str(len(taglist))+'\n')
        else:
            sys.stdout.write('state_num='+str(nums_tuple[0])+'\n')
        if len(wordlist) != nums_tuple[1]:
            sys.stdout.write('warning: different numbers of sys_num: claimed='+str(nums_tuple[1])+', real='+str(len(wordlist))+'\n')
        else:    
            sys.stdout.write('sys_num='+str(nums_tuple[1])+'\n')
        sum_probs = add_probs(transitions)
        sum_prob_emissions = add_probs(emissions)
        sum_init = 0
        for sts in start_state:
            sum_init += start_state[sts]
        if len(start_state) != nums_tuple[2]:
            sys.stdout.write('warning: different numbers of init_line_num: claimed='+str(nums_tuple[2])+', real='+str(len(start_state))+'\n')
        else:
            sys.stdout.write('init_line_num='+str(len(start_state))+'\n')
        if num_transitions != nums_tuple[3]:
            sys.stdout.write('warning: different numbers of trans_line_num: claimed='+str(nums_tuple[3])+', real='+str(num_transitions)+'\n')
        else:
            sys.stdout.write('trans_line_num='+str(num_transitions)+'\n')
        if num_emissions != nums_tuple[4]:
            sys.stdout.write('warning: different numbers of emiss_line_num: claimed='+str(nums_tuple[4])+', real='+str(num_emissions)+'\n')
        else:
            sys.stdout.write('emiss_line_num='+str(num_emissions)+'\n')
        if abs(sum_init-1) > 0.0001:
            sys.stdout.write('warning: the init_prob_sum is '+str(sum_init)+'\n')
        for state_pair in sum_probs:
            if abs(sum_probs[state_pair] - 1) > 0.0001:
                sys.stdout.write('warning: the trans_prob_sum for state '+state_pair+' is '+str(sum_probs[state_pair])+'\n')
        
        for state_tag in transitions:
            if state_tag not in emissions:
                tag_split = state_tag.split('_')
                if len(tag_split) == 1 and tag_split[0] not in taglist:
                    sum_prob_emissions[tag_split[0]] = 0
                elif len(tag_split) == 2 and tag_split[1] not in taglist:
                    sum_prob_emissions[state_tag] = 0

        for state_pair in sum_prob_emissions:
            if abs(sum_prob_emissions[state_pair] - 1) > 0.0001:
                sys.stdout.write('warning: the emiss_prob_sum for state '+state_pair+' is '+str(sum_prob_emissions[state_pair])+'\n')
