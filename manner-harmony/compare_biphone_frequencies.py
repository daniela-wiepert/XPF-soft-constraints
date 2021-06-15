import pandas as pd 
import os 
from collections import defaultdict
import csv
import json 

def main():
    lang_codes = []
    with open("lang_codes.tsv", 'r') as fin:
        reader = csv.reader(fin, delimiter='\t')
        lang_codes = list(reader)

    for lang_code in lang_codes: 
        lang_code = lang_code[0]
        print("lang code: ", lang_code)

        # read in natural word list 
        natural_words = []
        with open('word_lists/' + lang_code + '_word_list.tsv', 'r', encoding='utf8', newline='') as fin:
            reader = csv.reader(fin, delimiter='\t')
            natural_words = list(reader)
        filtered_lexicon = list(filter(lambda x: 3 <= len(x[0].split(" ")) <= 6, natural_words))
        filtered_lexicon = list(filter(lambda x: not ('@' in x[0].split(" ")), filtered_lexicon))

        natural_biphone_count = defaultdict(int)
        prev_phon = '[_w'
        for wd in filtered_lexicon:
            for phon in wd[0].split(" "):
                natural_biphone_count[prev_phon + '_' + phon] += 1
                prev_phon = phon
            natural_biphone_count[prev_phon + '_' + 'w_]'] += 1

        total_natural_biphones = sum(natural_biphone_count.values())
        natural_biphone_freq = {}
        for k, v in natural_biphone_count.items():
            natural_biphone_freq[k] = v / total_natural_biphones

        # read in generated words 
        generated_words = {}
        with open('generated_words/' + lang_code + '_generated_words.json', 'r', encoding='utf8') as fin:
            generated_words = json.load(fin)

        generated_words = generated_words.keys() 
        generated_biphone_count = defaultdict(int)
        prev_phon = None
        for wd in generated_words:
            for phon in wd.split(" "):
                if prev_phon != None:
                    generated_biphone_count[prev_phon + '_' + phon] += 1
                prev_phon = phon

        total_generated_biphones = sum(generated_biphone_count.values())
        generated_biphone_freq = {}
        for k, v in generated_biphone_count.items():
            generated_biphone_freq[k] = v / total_generated_biphones

        with open('biphone_frequencies/' + lang_code + '_generated_frequencies.json', 'w', encoding='utf8') as fout:
            json.dump(generated_biphone_freq, fout, ensure_ascii=False)

        with open('biphone_frequencies/' + lang_code + '_natural_frequencies.json', 'w', encoding='utf8') as fout:
            json.dump(natural_biphone_freq, fout, ensure_ascii=False)
    return None 

if __name__ == "__main__":
    main()