1. I use dictionary to store the input FST.
For convenience, I store the input FST in three different dictionaries.
a) is a dictionary with keys of (input state, input symbol, output state), and returns a list of possible probabilities
b) is a dictionary with keys of (input state, input symbol), and returns a list of possible output states
c) is a dictionary with keys of (input state, input symbol, output state), and returns a list of pairs (output symbol, proabbility)

2. I have to change the start probability part of the Viterbi Algorithm for HMM since in FST we have a start state, we can use that to generate possible initial states and assign corresponding start probability for them.
Also, I use a separate transducer to do the transducing work for FST. After the Viterbi Algorithm outputs the highest probability and corresponding path, I use the path information and transition functions to transduce the input words to generate output.
Another thing to notice is that general Viterbi Algorithm does not have an “end state” and we are just find the least path assuming each state can be an “end state”. In FST, we have a designated “end state” and we need that output probability for our FST.