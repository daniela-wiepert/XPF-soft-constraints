from collections import Counter, defaultdict
import pandas as pd
import ngram_model
import csv
import os
import json
'''
This file should calculate a set of all possible artificial words,
up to an arbitrary length, based on the n-gram model probabilities. 
Each artificial word should also be assigned its probability score. 
'''

phoneme_features = pd.read_csv("data/phoible_unique_phonemes.csv")

# global variable
# key is a generated word
# value is probability of that word
word_dict = {}

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

def generate_consonant(cv_model, c_model, v_model, wordlen=8, context='', n=4, current_prob=None):
    context = context.split(" ")
    n_context = context[-n:]
    n_context = [consonant_representation(phoneme) for phoneme in n_context]
    seg_counts = c_model.get(" ".join(n_context)) # dictionary of new segments 
    total_count = sum(seg_counts.values())
    for seg in seg_counts.keys(): # going through all possible predicted consonants
        new_context = " ".join(context) + " " + seg
        prob = seg_counts[seg] / total_count
        # continue generating the rest of this word
        generate_lexicon(cv_model, c_model, v_model, wordlen, new_context, n, current_prob * prob)

def generate_phoneme(model, wordlen=10, context='', n=3, current_prob=None):
    context = context.split(" ")
    n_context = context[-n:]
    seg_counts = model.get(" ".join(n_context)) # dictionary of new segments 
    total_count = sum(seg_counts.values())
    for seg in seg_counts.keys(): # going through all possible predicted next phonemes
        new_context = " ".join(context) + " " + seg
        prob = seg_counts[seg] / total_count
        # continue generating the rest of this word
        if current_prob:
            new_prob = current_prob * prob
        else: 
            new_prob = prob
        generate_lexicon(model, wordlen, new_context, n, new_prob)

def initial_context_prob(model, initial_context):
    freq = sum(model[initial_context].values())
    total_count = 0
    for k, v in model.items():
        if k[:3] == "[_w":
            total_count += sum(v.values())
    prob = freq / total_count
    return prob

def generate_lexicon(model, wordlen=10, context="", n=3, current_prob=None):
    '''
    Generate all possible words for this set of models. 

    Params: 
     - cv_model: consonant-vowel model dictionary (see ngram_model.py)
     - c_model: consonant model dictionary (see ngram_model.py)
     - v_model: vowel model dictionary (see ngram_model.py)
     - wordlen: cutoff length for generated words (including [_w and ]_w)
     - context: string representation of entire word up to this point 
                (not the previous n segs, but the entire word)
     - n: length of model's prior context
     - current_prob: the probability of generating the word (context) up till this point

    Returns:
     - Nothing, modifies global dictionary word_dict
    '''
    global word_dict 

    if context == "": # there is no prior context, starting a new word
        for prev_context in model.keys():
            if prev_context[0:3] == '[_w':
                if model.get(prev_context) != None:
                    initial_prob = initial_context_prob(model, prev_context)
                    func_context = prev_context
                    generate_phoneme(model, wordlen, func_context, n, initial_prob) # TODO: Should there be an initial prob?
    else:
        if context[-3:] == "]_w":
            word_dict[context] = current_prob
        else:
            context = context.split(" ")
            if len(context) < wordlen:
                n_context = context[-n:] # getting only previous n segments
                n_context = " ".join(n_context)
                context = " ".join(context)

                if model.get(n_context) != None:
                    generate_phoneme(model, wordlen, context, n, current_prob)


def main():
    global word_dict 

    lang_codes = []
    with open("lang_codes.tsv", 'r') as fin:
        reader = csv.reader(fin, delimiter='\t')
        lang_codes = list(reader)

    for lang_code in lang_codes: 
        lang_code = lang_code[0]
        print("lang code: ", lang_code)

        with open("utf8_ngram_models/" + lang_code + "_model.json", 'r', encoding='utf8') as fin:
            model = json.load(fin)
        
        generate_lexicon(model)

        with open("generated_words/" + lang_code + "_generated_words.json", 'w', encoding='utf8') as fout:
            json.dump(word_dict, fout, ensure_ascii=False)

        # resetting the dictionary for the next language
        word_dict = {}
        
    return None


if __name__ == "__main__":
    main()