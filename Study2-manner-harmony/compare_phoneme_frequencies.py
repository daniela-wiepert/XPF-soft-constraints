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

        natural_phoneme_count = defaultdict(int)
        for wd in filtered_lexicon:
            for phon in wd[0].split(" "):
                natural_phoneme_count[phon] += 1

        total_natural_phons = sum(natural_phoneme_count.values())
        natural_phoneme_freq = {}
        for k, v in natural_phoneme_count.items():
            natural_phoneme_freq[k] = v / total_natural_phons

        # read in generated words 
        generated_words = {}
        with open('generated_words/' + lang_code + '_generated_words.json', 'r', encoding='utf8') as fin:
            generated_words = json.load(fin)

        generated_words = generated_words.keys() 
        generated_phoneme_count = defaultdict(int)
        for wd in generated_words:
            for phon in wd.split(" "):
                if not phon in ['[_w', ']_w']:
                    generated_phoneme_count[phon] += 1

        total_generated_phons = sum(generated_phoneme_count.values())
        generated_phoneme_freq = {}
        for k, v in generated_phoneme_count.items():
            generated_phoneme_freq[k] = v / total_generated_phons

        with open('phoneme_frequencies/' + lang_code + '_generated_frequencies.json', 'w', encoding='utf8') as fout:
            json.dump(generated_phoneme_freq, fout, ensure_ascii=False)

        with open('phoneme_frequencies/' + lang_code + '_natural_frequencies.json', 'w', encoding='utf8') as fout:
            json.dump(natural_phoneme_freq, fout, ensure_ascii=False)
    return None 

if __name__ == "__main__":
    main()