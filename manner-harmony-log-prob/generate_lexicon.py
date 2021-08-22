from collections import Counter, defaultdict
import pandas as pd
import ngram_model
import csv
import os
import json
import math
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
total_initial_context_count = 0

def generate_phoneme(model, wordlen=10, context='', n=3, current_prob=None):
    context = context.split(" ")
    n_context = context[-n:]
    seg_counts = model.get(" ".join(n_context)) # dictionary of new segments 
    total_count = sum(seg_counts.values())
    for seg in seg_counts.keys(): # going through all possible predicted next phonemes
        new_context = " ".join(context) + " " + seg
        prob = seg_counts[seg] / total_count
        log_prob = math.log(prob)

        # continue generating the rest of this word
        if current_prob:
            new_log_prob = current_prob + log_prob
        else: # TODO: When would current prob be none?
            new_log_prob = log_prob
        generate_lexicon(model, wordlen, new_context, n, new_log_prob)

def initial_context_prob(model, initial_context):
    global total_initial_context_count
    freq = sum(model[initial_context].values())
    prob = freq / total_initial_context_count
    log_prob = math.log(prob)
    return log_prob

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
     - current_prob: the log probability of generating the word (context) up till this point

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
                    generate_phoneme(model, wordlen, func_context, n, initial_prob)
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


def exp_log_prob():
    global word_dict

    for word, log_prob in word_dict.items():
        word_dict[word] = math.exp(log_prob)

def main():
    global word_dict 
    global total_initial_context_count

    ### if testing sample lexicons
    lang_codes = []
    with open('sample_lang_codes.tsv', 'r') as fin:
        reader = csv.reader(fin, delimiter='\t')
        lang_codes = list(reader)

    for lang_code in lang_codes: 
        lang_code = lang_code[0]
        print("lang code: ", lang_code)

        with open("sample_utf8_ngram_models/" + lang_code + "_model.json", 'r', encoding='utf8') as fin:
            model = json.load(fin)
        
        for k, v in model.items():
                if k[:3] == "[_w":
                    total_initial_context_count += sum(v.values())

        # populate word_dict with log probability of a word appearing in this language
        generate_lexicon(model)
        # convert the log probabilities back to normal probabilities
        exp_log_prob()

        with open("sample_generated_words/" + lang_code + "_generated_words.json", 'w', encoding='utf8') as fout:
            json.dump(word_dict, fout, ensure_ascii=False)

        # resetting the dictionary for the next language
        word_dict = {}
        total_initial_context_count = 0

    ###

    # lang_codes = []
    # with open("lang_codes.tsv", 'r') as fin:
    #     reader = csv.reader(fin, delimiter='\t')
    #     lang_codes = list(reader)

    # for lang_code in lang_codes: 
    #     lang_code = lang_code[0]
    #     print("lang code: ", lang_code)

    #     with open("utf8_ngram_models/" + lang_code + "_model.json", 'r', encoding='utf8') as fin:
    #         model = json.load(fin)
        
    #     for k, v in model.items():
    #             if k[:3] == "[_w":
    #                 total_initial_context_count += sum(v.values())

    #     # populate word_dict with log probability of a word appearing in this language
    #     generate_lexicon(model)
    #     # convert the log probabilities back to normal probabilities
    #     exp_log_prob()

    #     with open("generated_words/" + lang_code + "_generated_words.json", 'w', encoding='utf8') as fout:
    #         json.dump(word_dict, fout, ensure_ascii=False)

    #     # resetting the dictionary for the next language
    #     word_dict = {}
    #     total_initial_context_count = 0
        
    return None


if __name__ == "__main__":
    main()