I use hashtable(dictionary) to store the HMM.
I tried to encode the string into integers and decode them back into string. However, I am not sure how I should do this in Python and just leave without that…

For the initial probabilities, just store dict[state] = prob into the dictionary.
For the transition probabilities, store dict[from_state].append((to_state, prob)). Since multiple to_state is possible from a certain from_state, we have to store it in a list.

For the emission probabilities, store dict[from_state].append((symb, prob)).

When calculating the sum of probabilities from certain given from_state, simply go over all the possible to_state, prob combination in the list and sum them over.

The create_3gram_hmm.sh program runs relatively slow… It took around 4 mins to run the training data in patas.