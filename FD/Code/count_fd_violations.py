import csv
import os
import pandas as pd
import functools

phoneme_features = pd.read_csv("Data/resolved-phoible.csv")

obstruents = phoneme_features[phoneme_features['sonorant'] == "-"]

phoible_stops = obstruents[obstruents["continuant"] == '-']
phoible_affricates = set(phoible_stops[phoible_stops["delayedRelease"] == "+"]["Phoneme"])
phoible_stops = set(phoible_stops[phoible_stops["delayedRelease"] == "-"]["Phoneme"])
phoible_fricatives = set(obstruents[obstruents['continuant'] == '+']["Phoneme"])
phoible_voiced = set(obstruents[obstruents['periodicGlottalSource'] == '+']["Phoneme"])
phoible_voiceless = set(obstruents[obstruents['periodicGlottalSource'] == '-']["Phoneme"])
phoible_obstruents = set(obstruents[:]["Phoneme"])

def is_obstruent(phoneme):
    return int(phoneme in phoible_obstruents)

def is_voiced(phoneme):
    return int(phoneme in phoible_voiced)


def is_voiceless(phoneme):
    return int(phoneme in phoible_voiceless)

def voiced_final(word):
    '''
    Parameters:
     - word: A list of a single string of the phonemic form of a word, where phonemes
      are separated by spaces. For example, ['[_w t i p ]_w']

    Returns a Boolean indicating if there is a voiced final obstruent word finally. 
    '''
    word = word.split(" ")
    #TODO: CHECK THIS GETS THE RIGHT THING
    phon = word[-1]
    if word[-1] == "]_w":
        phon = word[-2]
    if is_obstruent(phon) and is_voiced(phon):
        return 1
    return 0

def main():
    lang_codes = []
    word_lists = []
    identity = '5000_3'

    with open("Data/lang_codes"+identity+".tsv", 'r') as fin:
        reader = csv.reader(fin, delimiter='\t')
        lang_codes = list(reader)

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
    
    for lang_code in lang_codes:
        lang_code = ''.join(lang_code)
        print("lang code: ", lang_code)

        for roots, dirs, files in os.walk('Data/artificial_baselines/' + lang_code):
            final_voiced_lst = []
            
            for f in files:
                baseline = [] # the list of words in this artificial baseline
                with open('Data/artificial_baselines/' + lang_code + '/' + f, 'r', encoding='utf8') as fin:
                    reader = csv.reader(fin, delimiter='\t')
                    baseline = list(reader)
                baseline = list(map(lambda x: x[0], baseline))
                baseline_len = len(baseline)
                                
                # Percent of FD violations
                final_voiced_lst.append(sum(map(voiced_final,baseline)) /baseline_len)
                
            if not os.path.exists('Data/distributions/'):
                os.makedirs('Data/distributions/')

            with open('Data/distributions/' + lang_code + '_artificial.csv', 'w') as fout:
                write = csv.writer(fout)
                write.writerow(['final_voiced_obstruents'])
                for i in range(len(final_voiced_lst)):
                    write.writerow([final_voiced_lst[i]])        

        natural_lexicon = split_list[lang_code]

        # natural_lexicon = list(map(lambda x: x, natural_lexicon))
        filtered_lexicon = list(filter(lambda x: 3 <= len(x.split(" ")) <= 8, natural_lexicon))
        filtered_lexicon_len = len(filtered_lexicon)

        final_voiced_val = sum(map(voiced_final, filtered_lexicon)) / filtered_lexicon_len
    
        with open('Data/distributions/' + lang_code + '_natural.csv', 'w') as fout:
            write = csv.writer(fout)
            write.writerow(['final_voiced_obstruents'])
            write.writerow([final_voiced_val])        

    return None

if __name__ == "__main__":
    main()