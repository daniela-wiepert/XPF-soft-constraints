import csv
import os
import pandas as pd
import functools

phoneme_features = pd.read_csv("data/phoible_unique_phonemes.csv")

continuants = phoneme_features[phoneme_features['continuant'] == "+"]
phoible_sibilants = set(continuants[continuants["strident"] == '+']["Phoneme"])
phoible_fricatives = set(continuants[continuants['approximant'] != '+']["Phoneme"])

def phoible_ipa(phoneme):    
    '''
    Some of the XPF IPA doesn't match the PHOIBLE IPA. 
    Resolving mismatches.
    '''
    phoible_affricates = {'tʃ': 't̠ʃ',
    "dʒ": 'd̠ʒ',
    "tʃʼ": 't̠ʃʼ',
    "tʃʰ": 't̠ʃʰ'}

    phoible_prenasals = {"ⁿ": "n",
                "ᵐ": "m",
                "ᵑ": "ŋ",
                "ᶯ": "ɳ",
                "ᶮ": "ɲ" }

    if phoible_affricates.get(phoneme) != None:
        return phoible_affricates[phoneme]
    elif phoible_prenasals.get(phoneme[0]) != None:
        return phoible_prenasals.get(phoneme[0]) + phoneme[1:]
    else:
        return phoneme

def is_fricative(phoneme):
    phoneme = phoible_ipa(phoneme)
    return int(phoneme in phoible_fricatives)

def is_sibilant(phoneme):
    phoneme = phoible_ipa(phoneme)
    return int(phoneme in phoible_sibilants)

def same_fricatives(word):
    '''
    Parameters:
     - word: A list of a single string of the phonemic form of a word, where phonemes
      are separated by spaces. For example, ['[_w t i p ]_w']

    Returns a Boolean indicating if there are multiple of the same fricative in the word. 
    '''
    fricatives = []
    for phoneme in word.split(" "):
        if is_fricative(phoneme):
            if phoneme in fricatives:
                return 1
            else:
                fricatives.append(phoneme)
    return 0

def different_fricatives(word):
    '''
    Parameters:
     - word: A list of a single string of the phonemic form of a word, where phonemes
      are separated by spaces. For example, ['[_w t i p ]_w']

    Returns a Boolean indicating if there are at least two different fricatives in the word. 
    '''
    fricatives = []
    for phoneme in word.split(" "):
        if is_fricative(phoneme):
            if phoneme not in fricatives: 
                fricatives.append(phoneme)
        if len(fricatives) >= 2:
            return 1
    return 0

def multiple_fricatives(word):
    '''
    Parameters:
     - word: A string of the phonemic form of a word, where phonemes are separated by spaces. For example, '[_w t i p ]_w'

    Returns a Boolean indicating if there are multiple fricatives in the word. 
    '''
    fricatives = []
    for phoneme in word.split(" "):
        if is_fricative(phoneme):
            fricatives.append(phoneme)
            if len(fricatives) >= 2:
                return 1
    return 0

def same_sibilants(word):
    '''
    Parameters:
     - word: A string of the phonemic form of a word, where phonemes are separated by spaces. For example, '[_w t i p ]_w'

    Returns a Boolean indicating if there are multiple of the same sibilant in the word. 
    '''
    sibilants = []
    for phoneme in word.split(" "):
        if is_sibilant(phoneme):
            if phoneme in sibilants:
                return 1
            else:
                sibilants.append(phoneme)
    return 0

def multiple_sibilants(word):
    '''
    Parameters:
     - word: A string of the phonemic form of a word, where phonemes are separated by spaces. For example, '[_w t i p ]_w'

    Returns a Boolean indicating if there are multiple sibilants in the word. 
    '''
    sibilants = []
    for phoneme in word.split(" "):
        if is_sibilant(phoneme):
            sibilants.append(phoneme)
            if len(sibilants) >= 2:
                return 1
    return 0

def main(n=3, wordlen=10):
    lang_codes = []
    with open("lang_codes.tsv", 'r') as fin:
        reader = csv.reader(fin, delimiter='\t')
        lang_codes = list(reader)

    for lang_code in lang_codes: 
        lang_code = lang_code[0]
        print("lang code: ", lang_code)

        for roots, dirs, files in os.walk('artificial_baselines/' + lang_code):
            same_fricatives_lst = []
            different_fricatives_lst = []
            multiple_fricatives_lst = []
            same_sibilants_lst = []
            multiple_sibilants_lst = []
            for f in files:
                baseline = [] # the list of words in this artificial baseline
                with open('artificial_baselines/' + lang_code + '/' + f, 'r', encoding='utf8') as fin:
                    reader = csv.reader(fin, delimiter='\t')
                    baseline = list(reader)
                baseline = list(map(lambda x: x[0], baseline))
                baseline_len = len(baseline)

                # Percent of OCP violations
                same_fricatives_lst.append(sum(map(same_fricatives, baseline)) / baseline_len)
                different_fricatives_lst.append(sum(map(different_fricatives, baseline)) / baseline_len)
                multiple_fricatives_lst.append(sum(map(multiple_fricatives, baseline)) / baseline_len)
                same_sibilants_lst.append(sum(map(same_sibilants, baseline)) / baseline_len)
                multiple_sibilants_lst.append(sum(map(multiple_sibilants, baseline)) / baseline_len)
            
            with open('distributions/' + lang_code + '_artificial.csv', 'w') as fout:
                write = csv.writer(fout)
                write.writerow(['multiple_same_fricatives', 'multiple_diff_fricatives', 'multiple_fricatives', 'multiple_same_sibilants', 'multiple_sibilants'])
                for i in range(len(same_fricatives_lst)):
                    write.writerow([same_fricatives_lst[i], different_fricatives_lst[i], multiple_fricatives_lst[i], same_sibilants_lst[i], multiple_sibilants_lst[i]])        

        natural_lexicon = []
        with open('word_lists/' + lang_code + '_word_list.tsv', 'r', encoding='utf8') as fin:
            reader = csv.reader(fin, delimiter='\t')
            natural_lexicon = list(reader)
        natural_lexicon = list(map(lambda x: x[0], natural_lexicon))
        filtered_lexicon = list(filter(lambda x: n-1 <= len(x.split(" ")) <= wordlen-2, natural_lexicon))
        filtered_lexicon_len = len(filtered_lexicon)

        same_fricatives_val = sum(map(same_fricatives, filtered_lexicon)) / filtered_lexicon_len
        different_fricatives_val = sum(map(different_fricatives, filtered_lexicon)) / filtered_lexicon_len
        multiple_fricatives_val = sum(map(multiple_fricatives, filtered_lexicon)) / filtered_lexicon_len
        same_sibilants_val = sum(map(same_sibilants, filtered_lexicon)) / filtered_lexicon_len 
        multiple_sibilants_val = sum(map(multiple_sibilants, filtered_lexicon)) / filtered_lexicon_len

        with open('distributions/' + lang_code + '_natural.csv', 'w') as fout:
            write = csv.writer(fout)
            write.writerow(['multiple_same_fricatives', 'multiple_diff_fricatives', 'multiple_fricatives', 'multiple_same_sibilants', 'multiple_sibilants'])
            write.writerow([same_fricatives_val, different_fricatives_val, multiple_fricatives_val, same_sibilants_val, multiple_sibilants_val])        

    return None

if __name__ == "__main__":
    main()