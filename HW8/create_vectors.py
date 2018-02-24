import sys
import operator
import os

if __name__ == "__main__":
    train_vector = open(sys.argv[1], 'w')
    test_vector = open(sys.argv[2],'w')
    ratio = sys.argv[3]
    for args in sys.argv[4:]:
        num_of_files = len([name for name in os.listdir(args) if os.path.isfile(os.path.join(args, name))])
        num_of_train = int(num_of_files * float(ratio))
        num_of_test = num_of_files - num_of_train
        i = 0
        for filename in sorted(os.listdir(args)):
            subdirect = args.split('/')
            ellips_direct = ".."
            """
            if len(subdirect) > 3:
                for j in subdirect[-3:]:
                    ellips_direct += "/"+str(j)
            print(ellips_direct)
            """
            targetLabel = subdirect[-1]
            with open("output_temp",'w') as output:
                os.system("python3 proc_file.py "+args+"/"+str(filename)+" "+str(targetLabel)+" "+"output_temp")
            with open("output_temp",'r') as input:
                for line in input:
                    if line != '\n':
                        if i < num_of_train:
                            train_vector.write(line)
                        else:
                            test_vector.write(line)
            i += 1

        
        

