import sys
import string

def generate_tuple(line,transitions):
	# This is a function storing the FSA
	# it returns a tuple, in which, the first element is the start state
	# the second element is the end state
	# the third element is a transition function(hash table)
	splitting = line.split()
	inState = splitting[0][1:]
	outState = splitting[1][1:]
	length = len(splitting[2])
	m = 0
	for i in range(1,length):
		if splitting[2][i] == '\"':
			m = i
	symbol = splitting[2][1:m]
	# The transition function has the following format:
	# f(input state, symbol) = output state
	# since the input can be a NFA, output state can be a list
	if (inState, symbol) in transitions:
		transitions[(inState,symbol)].append(outState)
	else:
		tmp = []
		tmp.append(outState)
		transitions[(inState,symbol)] = tmp
	return (inState,outState,symbol)

def process_input(line):
	# generate a list of input symbols
	# input symbols is either letter or number
	input_list = []
	"""
	for char in line:
		if char.isalpha() or char.isdigit():
			input_list.append(char)
	"""
	split = line.split(' ')
	split[len(split)-1] = split[len(split)-1][0:len(split[len(split)-1])-1]
	input_list = split
	return input_list

def check_transition(curState,transitions,input):
	# a function used to check if a transition function exists with given input
	# curState is the input state of check
	if (curState,input) in transitions:
		return transitions[(curState,input)]
	else:
		return None

def check_fsa(startState, endState, transitions, inputList):
	# check if the fsa matches the input
	# assuming the fsa is a DFA
	# Go over the inputList, and match the input symbol with the DFA
	# if nextState is in the endState and the current symbol is the last symbol
	# the DFA can accept this string
	curState = startState
	for i in range(0,len(inputList)):
		nextState = check_transition(curState,transitions,inputList[i])
		if nextState != None:
			if (nextState in endState) and i == len(inputList)-1:
				return True
			else:
				curState = nextState
		else:
			return False

def epsilon_move(inState, transitions, tmp):
	# correspond to the e-closure property
	# return a set of states that moving zero or more epsilon moves
	# from current state can reach
	for s in inState:
		if (s, '') in transitions:
			if len(transitions[(s,'')]) == 1:
				tmp.add(transitions[(s,'')][0])
				epsilon_move(transitions[(s,'')][0],transitions,tmp)
			if len(transitions[(s,'')]) > 1:
				for p in transitions[(s,'')]:
					tmp.add(p)
					epsilon_move(p,transitions,tmp)
		else:
			continue
	return tmp.union(inState)

def set_to_state(stateSet):
	# convert a set to a state
	output = ''
	for s in stateSet:
		output += s
	return output

def sett_one(OneSet):
	# extract the set element if the set only has one
	if len(OneSet) == 1:
		tmp = OneSet.pop()
		OneSet.add(tmp)
		return tmp
	else:
		return None

def state_to_set(states):
	# convert a state to a set
	output = set([])
	for s in states:
		output.add(s)
	return output

def move_set(state, transitions, symbol):
	# Given the current state and symbol
	# give a set of states that such a move can reach
	move_out = set([])
	for s in state:
		if (s,symbol) in transitions:
			move_out = move_out.union(state_to_set(transitions[(s,symbol)]))
		else:
			continue
	return move_out

def nfa_to_dfa (startState, endState, transitions, stateList, symbolList):
	# convert a NFA to DFA
	newStartState = set([])
	empty = set([])
	# Mark the new start state to be the e-closure(startState)
	newStartState = epsilon_move(startState, transitions, empty)
	# Maintain a list of sets (states)
	setList = []
	setList.append(newStartState)
	# Make a new hash table for the new transition function
	newTransitions = dict()
	newEndState = []
	# remove *e* from our symbol list first since DFA does not have *e*
	if '' in symbolList:
		symbolList.remove('')
	for T in setList:
		for a in symbolList:
			S = set([])
			# if there is no path that the pair Move(T,a) can return
			# Skip this symbol and go to the next 
			if len(move_set(T,transitions,a)) == 0:
				continue
			else:
				# S = e-closure(Move(T,a))
				S = epsilon_move(move_set(T,transitions,a),transitions, S)
				if S not in setList:
					setList.append(S)
				t = set_to_state(T)
				s = set_to_state(S)
				# convert the set to state and add it to the new transition function
				newTransitions[(t,a)] = s

	# if the state includes the original end state, it is also an end state
	for S in setList:
		for i in S:
			if i == endState:
				s = set_to_state(S)
				newEndState.append(s)
	newStartState = set_to_state(newStartState)
	return (newStartState,newEndState,newTransitions)

def output_generator(input,sign):
	if (len(input)<12):
		output_str = input + (' '*(12-len(input))) + "=> " + sign
	else:
		output_str = input + ('\t' + '=> ' + sign)
	return output_str

if __name__ == "__main__":
	input_fsa = sys.argv[1]
	input_file = sys.argv[2]
	startState = None
	endState = None
	transitions = {}
	stateList = []
	symbolList = []
	with open(input_fsa,'r') as fsa:
		# Store the fsa in the data structure
		# the first line is the endState
		# the second char of the second line is the startState
		i = 0
		for line in fsa:
			if i == 0:
				"""endState = line[0]
				stateList.append(line[0])"""
				endState = line[0:len(line)-1]
				stateList.append(endState)
			if i == 1 and line[0] == '(':
				"""
				startState = line[1]
				stateList.append(line[1])
				"""
				split = line.split(' ')
				startState = split[0][1:len(split[0])-1]
			if i != 0:
				tuple = generate_tuple(line,transitions)
				if tuple[0] not in stateList:
					stateList.append(tuple[0])
				if tuple[1] not in stateList:
					stateList.append(tuple[1])
				if tuple[2] not in symbolList:
					symbolList.append(tuple[2])
			i += 1
	# convert NFA to DFA
	tuple_2 = nfa_to_dfa(startState,endState,transitions,stateList,symbolList)
	print(tuple_2)
	with open(input_file,'r') as symbList:
		for line2 in symbList:
			if (line2[len(line2)-1] == "\n"):
				outputStr = line2[:len(line2)-1]
			else:
				outputStr = line2
			if line2 == '*e*':
				if tuple_2[0] in tuple_2[1]:
					output_line = output_generator(outputStr,"yes")
				else:
					output_line = output_generator(outputStr,"no")
			else:
				processList = process_input(line2)
				print('haha',processList)
			# check if the DFA accepts the string and generate output
				if check_fsa(tuple_2[0], tuple_2[1], tuple_2[2], processList):
					output_line = output_generator(outputStr,"yes")
				else:
					output_line = output_generator(outputStr,"no")
			print (output_line)
