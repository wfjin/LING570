import sys

if __name__ == "__main__":
    pos_tag = sys.stdin.readlines()
    for line in pos_tag:
        split1 = line.split(' => ')
        words = split1[0].split(' ')
        tags = split1[1].split(' ')
        output_string = ""
        for i in range(1, len(tags)-2):
            tags_split = tags[i].split('_')
            word_tag = words[i-1]+'/'+tags_split[1]+' '
            output_string += word_tag
        tags_split_last = tags[len(tags)-2].split('_')
        word_tag_last = words[len(tags)-3]+'/'+tags_split_last[1]+'\n'
        output_string += word_tag_last
        sys.stdout.write(output_string)
