import re
import string
import sys

# Check if it is abbreviation for months
def date_checker(input):
    if (len(input) == 3):
        months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        if input not in months:
            return False
        else:
            return True
    else:
        return False

# Check if it is a number, including numbers separtaed by decimal and comma
# including negative numbers
def num_checker(input):
    format = re.compile("^-?[0-9]{1,3}(,[0-9]{3})*(\.[0-9]+)?$")
    isnumerical = re.match(format,input)
    return isnumerical

# Check if it is some form of the special cases
def web_checker(input):
    # check if it is an email address
    format = re.compile("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$")
    isemail = re.match(format,input)
    # check if it is an website address
    format2 = re.compile("^(http\:\/\/|https\:\/\/)?([a-z0-9][a-z0-9\-]*\.)+[a-z0-9][a-z0-9\-]*$")
    iswebsite = re.match(format2,input)
    # check if it is a path in form of /usr/dir/dropbox
    format3 = re.compile("^(.*/)([^/]*)$")
    ispath = re.match(format3,input)
    # check if it is a path in form of C:\usr\dir
    format4 = re.compile("^(.*\\\\)([^\\\\]*)$")
    ispath2 = re.match(format4,input)
    return (isemail or iswebsite or ispath or ispath2)

#check if there is an apostrophe in the word
def apos_checker(input):
    for char in input:
        if char != "\'":
            continue
        else:
            return True
        return False

def apos_rearrange(input):
    output = ''
    i = 0
    #go over the word, one by one letter
    for char in input:
        n = len(output)
        if char != "\'":
            output = output + char
            i += 1
        else:
            if i+1 < len(input):
                if input[i+1] == 't' and input[i-1] == 'n':
                    # check if it is in the form n't, follow the rule and tokenize it
                    output = output[:(n-1)] + " n\'"
                    i += 1
                    continue
                if input[i+1] != 't':
                    # if it is not in the form n't, just tokenize it
                    output = output + " \'"
                    i += 1
                    continue
            else:
                # if ' is the last char of the word, do not tokenize
                output = output+"\'"
                i += 1
                break
    return output

# helper function to handle some special cases, where non-tokenizable items are followed by a punctuation
def word_end(input):
    punctuation = string.punctuation.replace('/', '').replace('-', '').replace('+', '').replace('\'','')
    if input[len(input)-1] in punctuation:
        return input[:len(input)-1]+' '+input[len(input)-1]
    else:
        return input

# check if it is an abbreviation in the list
def abbrev_checker(input):
    filename2 = sys.argv[1]
    with open(filename2, 'r') as f:
        for line in f:
            for word in line.split():
                if input == word:
                    return True
    return False;

# check if it is a short-hand for name
# in the form A. , A.B. ,
def name_checker(input):
    format = re.compile("^([A-Z]\.)+")
    isname = re.match(format,input)
    return isname

# check if there is a hyphen in the word
def hyphen_checker(input):
    if (input[0] == "-"):
        return False
    for char in input:
        if char != "-":
            continue
        else:
            return True
        return False

def hyphen_place(input):
    output = ''
    i = 0
    for char in input:
        n = len(output)
        if char != "-":
            output = output + char
            i += 1
        else:
            if i+1 < len(input):
                if input[i+1].isalpha() and input[i-1] != "-": 
                #if the char after - is a letter and before - is not -
                    output = output + " - "
                    # separate the word before/after -
                    i += 1
                    continue
                if input[i+1] == "-":
                   # if it is a dash, do not separate it and tokenize it 
                    output = output + "--"
                    i = i + 3
                    continue
                if input[i-1].isdigit() and input[i+1].isdigit:
                    # if - is used as a minus sign between 2 numbers
                    # do not separate it
                    output = output + "-"
                    i += 1
                    continue
            else:
                break
    return output

# check if there is a / in the word
# in order not to confuse with the path, there is at most 1 slash in 1 word
def slash_checker(input):
    j = input.count("/")
    if j == 1:
        return True
    else:
        return False

def slash_separator(input):
    output = ''
    i = 0
    j = 0
    format = re.compile("^[A-Z]$")
    for char in input:
        n = len(output)
        if char != "/":
            i += 1
        else:
            if i+1 < len(input):
                if re.match(format,input[i+1]) and input[i-1].isalpha():
                # if the letter before/after / is both Capitailized letter
                # separate it and record the position of /
                # I know this is not a perfect solution, in order to avoid conflicts with paths
                # this is the best way I can think up right now
                    j = i
                    i += 1
                    break;
                else:
                    i += 1
                    break;
            else:
                break
    return j

if __name__ == "__main__":
        for line in sys.stdin:
            punctuation = string.punctuation.replace('/', '').replace('-', '').replace('+', '')
            #If it is an emtpy line, simply print another empty line
            if len(line.strip()) == 0 :
                print("\n",end = '')
                continue
            #initialize the output for each line
            output_line = ""
            for word in line.split():
                # if the word is a single &, tokenize it
                if word == "&":
                    output_line = output_line + " &"
                    continue 
                # if the first char in the word is ", tokenize it and process the rest of the word
                if word[0] == "\"":
                    output_line = output_line + " \""
                    word = word[1:]

                # if there is a slash in a word, tokenize it and process the rest of the word
                if slash_checker(word):
                    j = slash_separator(word)
                    output_line = output_line + " " + word[:j] + " /"
                    word = word[(j+1):] 

                # if there is a apostrophe in the word, pass it to the rearrange function
                if apos_checker(word):
                    output_line = output_line + " " + word_end(apos_rearrange(word))
                    continue

                # if the word is started with $, and the rest is numbers, tokenize both
                #if word[0] == '$' and num_checker(word[1:]):
                if word[0] == '$' and word[1].isdigit(): 
                    output_line = output_line + " " + '$' + " " + word_end(word[1:])
                    continue

                if len(word) > 2:
                    if word[0].isalpha() and word[1] == '$' and word[2].isdigit():
                        output_line = output_line + " " + word[0] + '$' + " " + word_end(word[2:])
                        continue
                    if len(word) > 3:
                        if word[0].isalpha() and word[1].isalpha() and word[2] == '$' and word[3].isdigit():
                            output_line = output_line + " " + word[0] + word[1] + '$' + " " + word_end(word[3:])
                            continue

                # if there is a number in the word, and it is in the end of the word followed by % and 
                # a punctuation, do not tokenize %
                if num_checker(word[:len(word)-2]) and word[len(word)-2] == "%" and word[len(word)-1] in punctuation:
                    output_line = output_line + " " + word[:len(word)-1] + " " + word[len(word)-1]
                    continue
                
                # if the number if followed by %, do not tokenize it
                if num_checker(word[:len(word)-1]) and word[len(word)-1] == "%":
                    output_line = output_line + " " + word[:len(word)-1] + "%"
                    continue

                # if the number is followed by symbols other than % and numbers, tokenize it 
                if num_checker(word[:len(word)-1]) and word[len(word)-1] != "%" and (num_checker(word) == False):
                    output_line = output_line + " " + word[:len(word)-1] + " " + word[len(word)-1]
                    continue

                if num_checker(word):
                    output_line = output_line + " " + word
                    continue

                # check if it is shorthand for name or an abbreviation, tokenize correspondingly
                if name_checker(word[:len(word)-1]) and word[len(word)-1] != '.' and word[len(word)-1] in punctuation:
                    output_line = output_line + " " + word[:len(word)-1] + " " + word[len(word)-1]
                    continue
                if name_checker(word):
                    output_line = output_line + " " + word
                    continue
                if abbrev_checker(word[:len(word)-1]) and word[len(word)-1] in punctuation:
                    output_line = output_line + " " + word[:len(word)-1] + " " + word[len(word)-1]
                    continue
                if abbrev_checker(word):
                    output_line = output_line + " " + word
                    continue

                # check if it is a month or other special web forms and tokenize correspondingly
                if date_checker(word):
                    output_line = output_line + " " + word
                    continue
                if web_checker(word):
                    output_line = output_line + " " + word
                    continue
                if web_checker(word[:len(word)-1]) and word[len(word)-1] in punctuation:
                    output_line = output_line + " " + word[:len(word)-1] + " " + word[len(word)-1]
                    continue

                # if there is hyphen, tokenize correspondingly
                if hyphen_checker(word):
                    output_line = output_line + " " + word_end(hyphen_place(word))
                    continue

                # if the word is in other forms, tokenize it with punctuation
                output_word = ''
                for letter in word:
                    if letter in punctuation:
                        output_word = output_word + " " + letter
                    else:
                        output_word = output_word + letter

                output_line = output_line + " " + output_word

            print(output_line)
