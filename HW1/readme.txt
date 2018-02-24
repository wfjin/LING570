After running the required commands, the outputs are:
The number of tokens in ex2: 39824
The number of tokens in ex2.tok: 47592
The number of lines in ex2.voc: 10425
The number of lines in ex2.tok.voc: 7774

Also, please note that make_voc.sh first sort the list of tokens according to the frequecny (stated in the spec), then by the time of appearance in the original text (not stated in the spec). That is to say, if tokens have the same frequency, they are sorted by their time of appearance.