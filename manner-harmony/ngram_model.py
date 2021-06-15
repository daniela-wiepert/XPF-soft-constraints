from collections import Counter, defaultdict
import pandas as pd
import os
import csv
import json

phoneme_features = pd.read_csv("data/phoible_unique_phonemes.csv")

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

def not_in_phoible(phoneme):
    '''
    If original phoneme is not in PHOIBLE, try to determine a close match. 
    A close match is acceptable in these cases since we only want to know if it's a consonant or a vowel.
    '''
    if phoneme == "":
        # if no other guess can be made, guess that it's a consonant
        return 'C'

    # PHOIBLE often has errors with phonemes that are represented with multiple IPA letters
    # like geminated palatalized affricates
    # so we're trying to find the nearest match by either removing the first or last part of that IPA representation
    # which shouldn't affect recognition as either a consonant or a vowel
    row = phoneme_features[phoneme_features["Phoneme"] == phoneme[1:]]
    
    if not row.empty:
        return 'C' if row["SegmentClass"].item() == 'consonant' else 'V'
    else:
        row = phoneme_features[phoneme_features["Phoneme"] == phoneme[:-1]]
        if not row.empty:
            return 'C' if row["SegmentClass"].item() == 'consonant' else 'V'
        else:
            return not_in_phoible(phoneme[1:-1])

def nphone_model(wordseglist, n=3, wordlen=10):
    '''
    Create n-gram models for the given word list of phonemes. 
    
    Params: 
     - wordseglist: a list of words, where each word is a list of a string of the IPA representation
                    such as [["b a"], ["d o"]]
     - n: Number of preceding segments in context
     - wordlen: Maximum length of words to use, including the word-initial and word-final tokens

    Returns:
     - consonant_vowel: A dictionary representing the CV n-gram model. Each key is a string representing
                        the context (perfect representation of n segments). Each value is another dictionary,
                        where the keys are whether the next segment is consonant, vowel, or word-final token, 
                        and the values are the counts. 
     - consonant: A dictionary representing the consonant n-gram model. Each key is a string representing
                        the context (imperfect representation of n segments). Each value is another dictionary,
                        where the keys are the next consonant, and the values are the counts. 
     - vowel: A dictionary representing the vowel n-gram model. Each key is a string representing
                        the context (perfect representation of n segments). Each value is another dictionary,
                        where the keys are the next vowel, and the values are the counts. 
    '''
    model = {}

    prev_context = []
    for word in wordseglist: # each word is a list of exactly one string, the word
        prev_context = ['[_w'] # start of word

        # don't use words that aren't perfectly translated to IPA
        if '@' in word[0].split(" "):
            continue 

        # don't use words that aren't the same length as generated words 
        # n - 1 because [_w is included in generated words
        # wordlen - 2 because both [_w and ]_w are included in generated words
        if len(word[0].split(" ")) < (n - 1) or len(word[0].split(" ")) > (wordlen - 2):
            continue

        word[0] = word[0].replace(" ː", "ː")
        for phoneme in word[0].split(" "): 
            if len(prev_context) == n:
                str_context = " ".join(prev_context)
                if model.get(str_context) is None:
                    model[str_context] = defaultdict(int)
                model[str_context][phoneme] += 1

                prev_context.pop(0) # remove earliest segment from context
            # update context
            prev_context.append(phoneme)

        # add word-final context once you've reached the end of the word
        if len(prev_context) >= n:
            str_context = " ".join(prev_context)
            if model.get(str_context) is None:
                model[str_context] = defaultdict(int)
            model[str_context][']_w'] += 1
    return model

def main():
    lang_codes = []
    for roots, dirs, files in os.walk('word_lists'):
        for f in files: 
            with open("word_lists/" + f, newline='') as fin:
                lang_code = f.split("_")[0]
                lang_codes.append([lang_code])
                
                print("lang_code: ", lang_code)
                
                reader = csv.reader(fin, delimiter='\t')
                word_list = list(reader)
                model = nphone_model(word_list)             

                with open("utf8_ngram_models/" + lang_code + "_model.json", 'w', encoding='utf8') as fout:
                    json.dump(model, fout, ensure_ascii=False)

    # a list of all language codes used in this analysis
    with open("lang_codes.tsv", 'w', newline='') as f:
        write =  csv.writer(f, delimiter="\t")
        write.writerows(lang_codes)

    return None 

if __name__ == "__main__": 
    main()