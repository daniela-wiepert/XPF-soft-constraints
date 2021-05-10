import pandas as pd 
import os 
from collections import defaultdict
import csv
import json 

def main():
    word_lists = []
    identity ='5000_3'   ##TODO: CHANGE THIS????
    #identity = 'practice'
    f_name = "Data/word_list"+identity+".tsv"

    tsv_file = open(f_name)
    read_tsv = csv.reader(tsv_file, delimiter="\t")

    for line in read_tsv:
        line[1]=line[1].strip('\n')
        word_lists.append(line)

    
    word_lists = word_lists[1:]
    split_list = {}
    l = []
    for i in range(len(word_lists)):
        lang_code = word_lists[i][0]
        if split_list.get(lang_code) is None:
            split_list[lang_code] = [word_lists[i][1]]
        else: 
            split_list[lang_code].append(word_lists[i][1])

    for lang in split_list:
        print(lang)
        natural_words = split_list[lang]

        # read in natural word list 

        filtered_lexicon = list(filter(lambda x: 3 <= len(x.split(" ")) <= 8, natural_words))
        filtered_lexicon = list(filter(lambda x: not ('@' in x.split(" ")), filtered_lexicon))

        natural_phoneme_count = defaultdict(int)
        for wd in filtered_lexicon:
            #TODO: check whether this should be wd[0] or just wd
            wd = wd.split(" ")
            #TODO: check if wd[-1] returns the last item
            #increment count for only final position
            natural_phoneme_count[wd[0]] += 1


        total_natural_phons = sum(natural_phoneme_count.values())
        natural_phoneme_freq = {}
        for k, v in natural_phoneme_count.items():
            natural_phoneme_freq[k] = v / total_natural_phons

        # read in generated words 
        generated_words = {}
        with open('Data/generated_words/' + lang + '_generated_words.json', 'r', encoding='utf8') as fin:
            generated_words = json.load(fin)

        generated_words = generated_words.keys() 
        generated_phoneme_count = defaultdict(int)
        for wd in generated_words:
            wd = wd.split(" ")
            generated_phoneme_count[wd[1]] += 1


        total_generated_phons = sum(generated_phoneme_count.values())
        generated_phoneme_freq = {}
        for k, v in generated_phoneme_count.items():
            generated_phoneme_freq[k] = v / total_generated_phons
        
        with open('Data/phoneme_frequencies/' + lang + '_generated_frequencies_initial.json', 'w', encoding='utf8') as fout:
            json.dump(generated_phoneme_freq, fout, ensure_ascii=False)
        with open('Data/phoneme_frequencies/' + lang + '_generated_counts_initial.json', 'w', encoding='utf8') as fout:
            json.dump(generated_phoneme_count, fout, ensure_ascii=False)
        with open('Data/phoneme_frequencies/' + lang + '_natural_frequencies_initial.json', 'w', encoding='utf8') as fout:
            json.dump(natural_phoneme_freq, fout, ensure_ascii=False)
        with open('Data/phoneme_frequencies/' + lang + '_natural_counts_initial.json', 'w', encoding='utf8') as fout:
            json.dump(natural_phoneme_count, fout, ensure_ascii=False)
    return None 

if __name__ == "__main__":
    main()