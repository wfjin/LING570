import sys
import string
import os

def checkLast4(label):
    if len(label) < 4:
        return False
    else:
        if label[-4:] == 'stem' or label[-4:] == 'form':
            return True
        else:
            return False

def generate_tuple(line, transitions, states, n):
    splitting = line.split()
    inState = splitting[0][1:]
    outState = splitting[1][1:]
    inSymbol = splitting[2][0:len(splitting[2])-2]

    if inState in states:
        inState = states[inState]
    else:
        states[inState] = 'q'+str(n)
        n = n + 1
        inState = states[inState]

    if outState in states:
        outState = states[outState]
    else:
        states[outState] = 'q'+str(n)
        n = n + 1
        outState = states[outState]
    if (inState, inSymbol) in transitions:
        transitions[(inState, inSymbol)].append(outState)
    else:
        tmp = []
        tmp.append(outState)
        transitions[(inState, inSymbol)] = tmp
    return (inState, inSymbol, outState, n)

if __name__ == "__main__":
    input_lex = sys.argv[1]
    input_morph = sys.argv[2]
    output_file = sys.argv[3]
    startStateMorph = None
    endState = None
    startState = None
    transitions = {}
    labelList = []
    wordList = []
    catList = []
    wordCat = {}
    wordEndState = {}
    oldState = {}
    startCat = {}
    stateList = []
    with open(input_lex,'r') as lex:
        wordState = 0
        for line in lex:
            lexSplit = line.split()
            if len(lexSplit) == 0:
                continue
            wordList.append(lexSplit[0])
            wordEndState[lexSplit[0]] = wordState + len(lexSplit[0])
            wordState += len(lexSplit[0])
            wordCat[lexSplit[0]] = lexSplit[1]
            if lexSplit[1] not in catList:
                catList.append(lexSplit[1])

    with open(input_morph,'r') as morph:
        i = 0
        n = 0
        for line in morph:
            if len(line) == 1 and line[0] == '\n':
                i += 1
                continue
            if i == 0:
                endState = line[0:len(line)-1]
            else:
                tuple = generate_tuple(line,transitions,oldState,n)
                if i == 1:
                    startState = tuple[0]
                if tuple[0] not in stateList:
                    stateList.append(tuple[0])
                if tuple[2] not in stateList:
                    stateList.append(tuple[2])
                if tuple[1] in catList:
                    if tuple[1] in startCat:
                        startCat[tuple[1]].append(tuple[2])
                    else:
                        tmp = []
                        tmp.append(tuple[2])
                        startCat[tuple[1]] = tmp
                n = tuple[3]
            i += 1
    endState = oldState[endState]
    fsa = open('fsa1','w')
    fsa.write(startState+'\n')
    state = 1
    for word in wordList:
        i = 0
        j = 0
        for i in range(0, len(word)):
            if i == 0:
                if len(word) != 1:
                    fsa.write('(w0 (w'+str(state)+' \"'+str(word[i])+'\" *e*))\n')
                if len(word) == 1:
                    fsa.write('(w0 (w'+str(state)+' \"'+str(word[i])+'\" \"'+wordCat[word]+'\"))\n')
                    break
            else:
                if i == len(word)-1:
                    fsa.write('(w'+str(state+j)+' (w'+str(state+j+1)+' \"'+str(word[i])+'\" \"'+wordCat[word]+'\"))\n')
                else:
                    fsa.write('(w'+str(state+j)+' (w'+str(state+j+1)+' \"'+str(word[i])+'\" *e*))\n')
                j += 1
            i += 1
        state = state + len(word)
        fsa.write('(w'+str(state-1)+' ('+startState+' *e* *e*))\n')
        fsa.write('(w'+str(state-1)+' (w0'+' *e*'+'))\n')
    fsa.close()
    fsa2 = open('fsa2','w')
    fsa2.write(endState+'\n')
    id = 0
    catList.append('*e*')
    for key in catList:
        for s in stateList:
            if (s,key) in transitions:
                for t in transitions[(s,key)]:
                    if key == '*e*':
                        fsa2.write('('+s+' ('+t+' *e*'+'))\n')
                    else:
                        fsa2.write('('+s+' ('+t+' \"'+key+'\"))\n')
    fsa2.close()   
    os.popen("carmel fsa1 fsa2 > "+output_file)              
    '''
                    if (len(suffixLabel[key]) == 1):
                        fsa.write('('+s+' ('+t+' \"'+suffixLabel[key]+'\"))\n')
                    else:
                        i = 0
                        for l in suffixLabel[key]:
                            if i == 0:
                                fsa.write('('+s+' (m'+str(id)+' \"'+suffixLabel[key][0]+'\"))\n')
                                id += 1
                            if i == 1:
                                fsa.write('(m'+str(id-1)+' (m'+str(id)+' \"'+suffixLabel[key][i]+'\"))\n')
                                id += 1
                            if i != 0 and i != 1:
                                fsa.write('(m'+str(id-1)+' (m'+str(id)+' \"'+suffixLabel[key][i]+'\"))\n')
                                id += 1
                            if i == len(suffixLabel[key])-1:
                                fsa.write('(m'+str(id-1)+' ('+endState+' '+'*e*'+'))\n')
                            i += 1
                    '''
