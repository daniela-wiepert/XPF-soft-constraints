#!/usr/bin/env python3

import subprocess
import argparse
import csv
import sys
from sys import stdin

def main(argv):
    parser =  argparse.ArgumentParser()
    ##
    ## Specify the language info - code, data files, etc.
    ##
    parser.add_argument("-l", "--lang-list", dest="langlist",
                        default='/mnt/z/Data/langs-list-03.tsv',
                        help="contains all data for a given language")
    ##
    ## Specify whether to use top 5000 words or top 10000 words
    ##
    parser.add_argument("-c", "--count-limit", dest = "countlimit", default = 5000,
                        help = "choose amount of most frequent words (top 5000 most frequent words/top 10000 etc.)")


    ##
    ## Specify second arg of stopatn
    ##
    parser.add_argument("-f", "--arg2", dest = "arg2", default = 3)

    ##
    ## Print Summary?
    ##
    parser.add_argument("-N", "--no-summary", dest="nosummary",
                        default=False, action="store_true",
                        help="suppress summary information")

    options = vars(parser.parse_args(argv))

    c = options["countlimit"]
    a = options["arg2"]

    f_name = 'counts' + str(c) + '_' + str(a) + '.tsv'                             #create file name for output

    with open(f_name, 'w', newline='') as f:                            #Prep TSV file
        write =  csv.writer(f, delimiter="\t")
        write.writerow(['Language', 'Phoneme', 'Onset', 'Coda', 'Total'])

    tsv_file = open(options["langlist"])
    read_list = csv.reader(tsv_file,delimiter="\t")

    num_languages = 0
    r = 0
    for row in read_list:                           #for each language
        if r != 0:                                  #first row contains headers - skip
            code = row[0]
            cmd1 = 'bzcat /mnt/z/' + row[7] + ' | bash /mnt/z/Code/stopatn.sh ' + str(c) + ' ' + str(a) + ' | python3 /mnt/z/Code/sumstats01.py -l /mnt/z/' + row[5]
            sub1 = subprocess.Popen(cmd1,shell=True,stdout=subprocess.PIPE)

            t = 0       #total words processed
            p = 0.0     #percent @ words

            for line in sub1.stdout:        #read output from sumstats01
                line.rstrip()
                info = line.split()
                check = info[1].decode("utf-8")
                i = info[-1].decode("utf-8")
                if check == 'processed':
                    t = int(i)
                if check == '%@':
                    p = float(i)

            if t >= int(c) and p <= 2.0:          #if total words >= 5000 and %@ words <= 2%
                # Getting the top 5000+ words for this language
                cmd = 'bzcat /mnt/z/' + row[7] + ' | sh /mnt/z/Code/stopatn.sh ' + str(c) + ' ' + str(a) + ' | python3 /mnt/z/Code/translate04.py -l /mnt/z/' + row[5] + ' -r - | cut -f2 | python3 wordseg.py'
                sub = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)

                word_list = []
                for line in sub.stdout:
                    line = line.rstrip()
                    word_list.append([line.decode("utf-8")])

                with open("word_lists/" + code + "_word_list.tsv", 'a+', newline='') as f:
                    write =  csv.writer(f, delimiter="\t")
                    write.writerows(word_list)

                num_languages += 1
        r += 1
    print("Language Count")
    print(num_languages)
    
if __name__ == "__main__":
    main(sys.argv[1:])
