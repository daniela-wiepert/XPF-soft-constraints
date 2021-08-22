from collections import Counter, defaultdict
import pandas as pd
#import ngram_modelfd
import csv
import os
import json
import numpy as np
'''
This file should calculate a set of all possible artificial words,
up to an arbitrary length, based on the n-gram model probabilities. 
Each artificial word should also be assigned its probability score. 
'''

# get phoneme features from PHOIBLE
# note the path is resolved-phoible.csv that is corrected for mismatches between phonemes in PHOIBLE and the XPF Corpus
phoneme_features = pd.read_csv("Data/resolved-phoible.csv")
phoneme_features.drop(["InventoryID", "Glottocode","ISO6393","LanguageName","SpecificDialect","GlyphID","Allophones","Marginal","Source"], axis="columns", inplace=True)
phoneme_features = phoneme_features.rename(columns={'periodicGlottalSource':'voice'})

# list of all feature names in PHOIBLE table
features = phoneme_features.copy()
features.drop(["Phoneme","voice"],axis="columns", inplace=True)
features = features.columns.values.tolist()

# global variables
word_dict = {} #dictionary of generated word: probability of word
to_feat = {} #dictonary of phoneme: feature representation 
phon_model = {} #dictionary of feature representation: {possible phonemes: # of occurrences}

def change_to_feat(phoneme):
    '''
    '''
    global to_feat
    if to_feat.get(phoneme) is None:
        return phoneme

    return to_feat.get(phoneme)


def reconstruct_phon(feat, previous):
    '''
    takes a feature and returns list of possible phonemes + their probabilities
    '''
    global phon_model
    poss_dict = phon_model.get(" ".join([previous,feat]))

    if poss_dict is None:
        return [''], [0.0]

    phon = list(poss_dict.keys())
    prob = list(poss_dict.values()) 
    
    return phon, prob


def reconstruct_con(context):
    '''
    takes a context with an imperfect representation and reconstructs it
    '''
    context = context.split(" ")
    length = len(context) - 1 
    phon = []
    prob = []
    final_phon = []
    final_prob = []

    # INITIAL FEATURE RECONSTRUCTION
    prev = context.pop(0)
    curr = context.pop(0)

    p,pr  = reconstruct_phon(curr,prev)
    pr = np.log(pr)

    for ph in p:
        phon.append([ph])
    prob.extend(pr)

    next_feat = context.pop(0)
    prev_len = 1
    
    while phon != []:
        prev_phon = phon.pop(0)
        prev_prob = prob.pop(0)
        if len(prev_phon) == length:
            final_phon.append(" ".join(prev_phon))
            final_prob.append(prev_prob)

        else:
            if len(prev_phon) > prev_len:
                prev_len += 1
                next_feat = context.pop(0)

            #reconstruct    
            p,pr = reconstruct_phon(next_feat,prev_phon[-1])
            pr = np.log(pr)

            for i in range(len(p)):
                new_phon = []
                new_phon.extend(prev_phon)
                new_phon.append(p[i])
                phon.append(new_phon) 
                prob.append(prev_prob + pr[i])

    return final_phon, final_prob


def make_contexts(poss,prob,contexts=[],context_prob=[]):
    '''
    all possible contexts
    '''
    con = []
    con_prob = []
    if poss == []:
        return contexts, context_prob
    elif contexts == []:
        p = poss[0]
        pr = prob[0]
        for i in range(len(p)):
            con.append(p[i])
            con_prob.append(pr[i])
    else:
        for i in range(len(contexts)):
            c = contexts[i]
            cpr = context_prob[i]
            p = poss[0]
            pr = prob[0]
            for j in range(len(p)):
                con.append(c + ' ' + p[j])
                con_prob.append(pr[j]+cpr)

    return make_contexts(poss,prob,con,con_prob)

def generate_phoneme(model, wordlen=8, context='', n=4, current_prob=None):
    context = context.split(" ")
    n_context = context[-n:]
    seg_counts = model.get(" ".join(n_context)) # dictionary of new segments 
    total_count = sum(seg_counts.values())
    in_seg = {}
    for seg in seg_counts.keys(): # going through all possible predicted consonants
        feat = change_to_feat(seg)
        if in_seg.get(feat) is None:
            in_seg[feat] = 0
        in_seg[feat] += seg_counts[seg]
    
    for seg in in_seg.keys():
        new_context = " ".join(context) + " " + seg
        prob = in_seg[seg] / total_count
        prob = np.log(prob)
        # continue generating the rest of this word
        generate_lexicon(model, wordlen, new_context, n, current_prob + prob)
    
def initial_context_prob(model, initial_context):
    '''
    get initial probabilites
    input: model  and initial context
    outpu: initial probability
    '''
    freq = sum(model[initial_context].values())
    total_count = 0
    for k, v in model.items():
        if k[:3] == "[_w":
            total_count += sum(v.values())
    prob = freq / total_count
    return np.log(prob)

def generate_lexicon(model, wordlen=8, context="", n=4, current_prob=None):
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
                    prob = initial_context_prob(model, prev_context)
                    func_context = prev_context
                    generate_phoneme(model, wordlen,func_context,n,prob)
                    break
    else:
        if context[-3:] == "]_w":
            # poss_contexts, poss_probs = reconstruct_con(context[:-4])
            # for i in range(len(poss_contexts)):
            #     word_dict['[_w ' + poss_contexts[i] + ' ]_w'] = current_prob + poss_probs[i]
            pass

        else:
            context = context.split(" ")
            if len(context) < wordlen:
                n_context = context[-n:] # getting only previous n segments
                n_context = " ".join(n_context)
                context = " ".join(context)
                print("n_context: ", n_context)

                if model.get(n_context) != None:
                    print("ASDFASDFASDFASDF")
                    generate_phoneme(model, wordlen, context, n, current_prob)
                                

def main():
    global word_dict 
    global to_feat
    global phon_model

    lang_codes = []
    identity = '5000_3'

    with open("Data/lang_codes"+identity+".tsv", 'r') as fin:
        reader = csv.reader(fin, delimiter='\t')
        lang_codes = list(reader)

    for lang_code in lang_codes:
        lang_code = ''.join(lang_code)
        print("lang code: ", lang_code)

        infile = './Data/utf8_ngram_models/'
        
        with open(infile + lang_code + "_model.json", 'r', encoding='utf8') as fin:
            model = json.load(fin)

        with open(infile + lang_code + "_phon_model.json", 'r', encoding='utf8') as fin:
            phon_model = json.load(fin)
        
        with open(infile + lang_code + "_to_feat.json", 'r', encoding='utf8') as fin:
            to_feat = json.load(fin)

        generate_lexicon(model)

        #exponentiate everything in the word dict
        print(len(word_dict))
        word_dict = {k:v for k,v in word_dict.items() if v != float('-inf')}
        print(len(word_dict))
        word_dict = {key: np.exp(value) for key, value in word_dict.items()}

        outfile  = './Data/generated_words/'
        if not os.path.exists(outfile):
            os.mkdir(outfile)
        with open(outfile + lang_code + "_generated_words.json", 'w', encoding='utf8') as fout:
            json.dump(word_dict, fout, ensure_ascii=False)

        # resetting the dictionariesfor the next languages
        word_dict = {}
        to_feat = {}
        phon_model = {}
        break


    return None


if __name__ == "__main__":
    main()