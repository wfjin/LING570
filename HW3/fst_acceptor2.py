import sys
import string
from decimal import Decimal

def generate_tuple(line, transitions1, transitions2, transitions3):
	# generate tuple for input state, output state, input symbol, output symbol
	# and corresponding probability
	# and update three kinds of transition functions respectively
    splitting = line.split()
    inState = splitting[0][1:]
    outState = splitting[1][1:]
    inSymbol = splitting[2]
    if len(splitting) == 5:
        outSymbol = splitting[3]
        length = len(splitting[4])
        prob = float(splitting[4][0:length-2])
    else:
        outSymbol = splitting[3][0:len(splitting[3])-2]
        prob = 1.0
	# transitions1 is a dictionary
	# keys are (input state, input symbol, output state)
	# generate a list of possible probabilities
    if (inState, inSymbol, outState) in transitions1:
        transitions1[(inState, inSymbol, outState)].append(prob)
    else:
        tmp1 = []
        tmp1.append(prob)
        transitions1[(inState, inSymbol, outState)] = tmp1
	# transition 2's keys are (input state, input symbol)
	# generate a list of output states
    if (inState, inSymbol) in transitions2:
        transitions2[(inState, inSymbol)].append(outState)
    else:
        tmp2 = []
        tmp2.append(outState)
        transitions2[(inState, inSymbol)] = tmp2
	# transition 3's keys are (input state, input symbol, output state)
	# generate a list of pairs (output symbol, probability)
    if (inState, inSymbol, outState) in transitions3:
        transitions3[(inState, inSymbol, outState)].append((outSymbol, prob))
    else:
        tmp3 = []
        tmp3.append((outSymbol, prob))
        transitions3[(inState, inSymbol, outState)] = tmp3
    return (inState, outState, inSymbol, outSymbol, prob)

def output_generator(input, sign):
    if len(input) < 12:
        output_str = input + (' '*(12-len(input))) + "=> " + sign
    else:
        output_str = input + ('\t' + '=> ' + sign)
    return output_str

def fullInZeros(transitions1, transitions2, transition3, stateList, inSymbol):
	# fill in zeros to transition functions
	# if (state, input symbol, state) is not in dict
	# assign probability 0 to it
	# if (input state, input symbol) is not in dict
	# assign the output state to be none
    for s in stateList:
        for ss in stateList:
            for y in inSymbol:
                if (s, y, ss) not in transitions1:
                    tmp = []
                    tmp.append(0)
                    transitions1[(s, y, ss)] = tmp
                    transitions3[(s, y, ss)] = None
                if (s, y) not in transitions2:
                    tmp = []
                    tmp.append(None)
                    transitions2[(s, y)] = tmp


def maxProb(transitions, inState, inSymbol, outState):
	# return the highest probability of all possible transitions
	# given input state, input symbol and output state
    result = transitions[(inState, inSymbol, outState)]
    if len(result) == 1:
        return result[0]
    else:
        max = -1
        for i in result:
            if i > max:
                max = i
        return max

def calc_viterbi(transitions1, transitions2, stateList, words, s, e):
	# calculate the viterbi probability
	# given two different kinds of transition functions, a list of states, input words,
	# and a start state s
	# construct a Viterbi table with len(words) rows and len(stateList) cols
	# V[r][c] means that the probability of r'th char in input words with final state c
    V = [{}]
    path = {}
	# startSymb is the possible states given the start state and the first char in input
    startSymb = transitions2[(s, words[0])]
	# fill out the "0" row of the viterbi table
	# if the state is in startSymb, assign it with corresponding probability
	# from the transition function
	# otherwise, set the prob to be 0
	# start the path to record
    for ss in stateList:
        V.append({})
        if ss in startSymb:
            V[0][ss] = maxProb(transitions1, s, words[0], ss)
            path[ss] = [ss]
        else:
            V[0][ss] = 0
            path[ss] = [ss]
	# go over the input word from pos 1
	# each iteration is to fill out the t th row of Viterbi table
    for t in range(1, len(words)):
        V.append({})
        newpath = {}
		# fill out the columns in t th row
        for y in stateList:
			# yy is "last" state
			# y is the "cuurent" state
			# the current viterbi probability = V[t-1][yy]* transitionProb from yy to y
			# find the maximum current viterbi probability and corresponding state
			# assign it to the table, update the path
            (prob, state) = max([(V[t-1][yy]*maxProb(transitions1, yy, words[t], y), yy) for yy in stateList])
            V[t][y] = prob
            newpath[y] = path[state]+[y]
        path = newpath
	# return the correct prob in the table and add the start state to the path
	#(prob,state) = max([(V[len(words)-1][y],y) for y in stateList])
    (prob, state) = (V[len(words)-1][e], e)
    return (prob, [startState]+path[state])

def transducer(transitions, tranStates, input, endState):
	# Having transition functions and states with the highest probability
	# transduce the input words
	# note that len(tranStates) = len(input)+1
	# initialize the output string
    output_string = ""
    for i in range(0, len(input)):
        maxsymb = None
        maxprob = -1
        for (s, p) in transitions[(tranStates[i], input[i], tranStates[i+1])]:
            if p > maxprob:
                maxprob = p
                maxsymb = s
		# find the maximum probability and corresponding output symbol
		# given input state, input symbol and output state
        if maxsymb == '*e*':
            output_string = output_string
        else:
            output_string = output_string + maxsymb + " "
    return output_string

if __name__ == "__main__":
    input_fst = sys.argv[1]
    input_file = sys.argv[2]
    startState = None
    endState = None
    transitions1 = {}
    transitions2 = {}
    transitions3 = {}
    stateList = []
    inSymbolList = []
    outSymbolList = []
    with open(input_fst, 'r') as fsa:
		# Store the fst in the data structure
		# the first line is the endState
		# the second char of the second line is the startState
        i = 0
        for line in fsa:
            if len(line) == 1 and line[0] == '\n':
                i += 1
                continue
            if i == 0:
                endState = line[0:len(line)-1]
                stateList.append(endState)
            if i == 1 and line[0] == '(':
                splitting = line.split()
                startState = splitting[0][1:]
                if startState not in stateList:
                    stateList.append(startState)
            if i != 0:
				# update the transition functions, stateList and symList
                tuple = generate_tuple(line, transitions1, transitions2, transitions3)
                if tuple[0] not in stateList:
                    stateList.append(tuple[0])
                if tuple[1] not in stateList:
                    stateList.append(tuple[1])
                if tuple[2] not in inSymbolList:
                    inSymbolList.append(tuple[2])
                if tuple[3] not in outSymbolList:
                    outSymbolList.append(tuple[3])
            i += 1
		# fill in zeros and none to the transition functions
        fullInZeros(transitions1, transitions2, transitions3, stateList, inSymbolList)
        words_input = open(input_file,'r')
        for line in words_input:
            if line[len(line)-1] == "\n":
                outputStr = line[:len(line)-1]
            else:
                outputStr = line
            splitting = line.split()
            try:
				# pair is (probability,states)
                pair = calc_viterbi(transitions1, transitions2, stateList, splitting, startState, endState)
				# transduce using the states from Viterbi
                if pair[1][len(pair[1])-1] != endState:
                    output_line = output_generator(outputStr, "*none* 0")
                else:
                    output2 = transducer(transitions3, pair[1], splitting, endState)
                    probability = "{:.3e}".format(Decimal(str(pair[0])))
                    output_line = output_generator(outputStr, output2+str(probability))
                print(output_line)
            except:
				# cases when calc_viterbi cannot run normally
				# which means the input is not accepted by the fst
                output_line = output_generator(outputStr, "*none* 0")
                print(output_line)
                pass
