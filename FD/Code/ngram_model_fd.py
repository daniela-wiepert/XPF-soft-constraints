from collections import Counter, defaultdict
import pandas as pd
import os
import csv
import json

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
to_feat = {} #dictonary of phoneme: feature representation 
phon_model = {} #dictionary of feature representation: {possible phonemes: # of occurrences}

def change_to_feat(phoneme, previous):
    '''
    Takes in a character string representing the IPA form of the phoneme and returns a feature representation of the phoneme based on PHOIBLE features
    Input: phoneme - character string representing current phoneme
           next - character string representing phoneme that follows
    Output: feature representation of the phoneme - character string ('feature1/[+,-,NA]|feature2/[+,-,NA]|etc...')
            each feature name/value pair is joined with '/' while separate feat/value pairs are joined with '|'
            can split the string representation using these characters
    '''
    global to_feat
    global phon_model

    # create and add feature representation to to_feat dictionary if not already in it
    if to_feat.get(phoneme) is None:
        row = phoneme_features[phoneme_features["Phoneme"] == phoneme]
        feat = []

    #creates feature representations for only obstruents 
        if not row.empty:
            if row["sonorant"].values.tolist()[0] == '-':
                for f in features:
                    t = row[f].values.tolist()[0]
                    feat.append(t+'/'+f)
                feat = '|'.join(feat)
                to_feat[phoneme] = feat             
            else:
                to_feat[phoneme] = phoneme
        else:
            to_feat[phoneme] = phoneme

    
    #get feature 
    feat = to_feat.get(phoneme)

    #context
    con = " ".join([previous, feat])
    #add feature to phoneme model if it doesn't already exist
    if phon_model.get(con) is None:
        phon_model[con] = defaultdict(int)

    # increment occurrence in phoneme model    
    phon_model[con][phoneme] += 1

    return feat


def nphone_model(wordseglist, n=4, wordlen=8):
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
        prev_phon = {}
        # don't use words that aren't perfectly translated to IPA
        if '@' in word.split(" "):
            continue 

        # don't use words that aren't the same length as generated words 
        # n - 1 because [_w is included in generated words
        # wordlen - 2 because both [_w and ]_w are included in generated words
        if len(word.split(" ")) < (n - 1) or len(word.split(" ")) > (wordlen - 2):
            continue

        word = word.replace(" ː", "ː")
        prev_p = ''
        str_context = ''
        for phoneme in word.split(" "): 
            if len(prev_context) == n:
                if prev_context[0] == "[_w":
                    f = ['[_w']
                    for i in range(len(prev_context)-1):
                        f.append(change_to_feat(prev_context[i+1],prev_context[i]))
                else:
                    con = [prev_phon[" ".join(prev_context)]]
                    con.extend(prev_context)
                    f = []
                    for i in range(len(prev_context)-1):
                        f.append(change_to_feat(prev_context[i+1],prev_context[i]))
               
                str_context = " ".join(f)
                if model.get(str_context) is None:
                    model[str_context] = defaultdict(int)
                model[str_context][phoneme] += 1

                prev_p = prev_context[0]
                prev_context.pop(0) # remove earliest segment from context
            
            # update context
            prev_context.append(phoneme)
            if len(prev_context) == n:
                prev_phon[" ".join(prev_context)] = prev_p

        # add word-final context once you've reached the end of the word
        # remove voicing information at end of the word
        if len(prev_context) >= n:
            f = []
            for i in range(len(prev_context)):
                if i==0:
                    f.append(change_to_feat(prev_context[i],prev_phon[" ".join(prev_context)]))
                else:
                    f.append(change_to_feat(prev_context[i],prev_context[i-1]))
            str_context = " ".join(f)
            if model.get(str_context) is None:
                model[str_context] = defaultdict(int)
            model[str_context][']_w'] += 1

    return model

def main():
    '''
    NOTE: this file handles reading in data differently
    #TODO: write down what code creates the word list used for this
    '''
    global to_feat
    global phon_model
    word_lists = []
    lang_codes = []
    identity ='5000_3'   ##TODO: change this depending on inputs to translate04.py
    f_name = "Data/word_list"+identity+".tsv"

    # READ IN THE WORD LIST
    tsv_file = open(f_name)
    read_tsv = csv.reader(tsv_file, delimiter="\t")
    for line in read_tsv:
        line[1]=line[1].strip('\n')
        word_lists.append(line)

    # SPLIT LIST PER LANGUAGE
    word_lists = word_lists[1:]
    split_list = {}
    l = []
    for i in range(len(word_lists)):
        lang_code = word_lists[i][0]
        if split_list.get(lang_code) is None:
            split_list[lang_code] = [word_lists[i][1]]
        else: 
            split_list[lang_code].append(word_lists[i][1])

    # GO THROUGH EACH LANGUAGE (can adjust the  word length  here)
    for lang in split_list:
        print(lang)
        lang_codes.append(lang)
        curr_list = split_list[lang] 
        
        model = nphone_model(curr_list,wordlen=10)

        outfile = "./Data/utf8_ngram_models/"
        if not os.path.exists(outfile):
            os.mkdir(outfile)

        # save output model
        with open(outfile + lang + "_model.json", 'w+', encoding='utf8') as fout:
            json.dump(model, fout, ensure_ascii=False)

        # CHANGE phon_model from  # occurrence to probability
        for feat in phon_model:
            total = sum(phon_model.get(feat).values(),0.0)
            phon_model[feat] = {k: v / total for k,v in phon_model.get(feat).items()}

        # save phon_model
        with open(outfile + lang + "_phon_model.json", 'w+', encoding='utf8') as fout:
            json.dump(phon_model, fout, ensure_ascii=False)
        
        # save feature conversion dict
        with open(outfile + lang + "_to_feat.json", 'w+', encoding='utf8') as fout:
            json.dump(to_feat, fout, ensure_ascii=False)

        # reset to_feat and phon_model after each language
        to_feat = {}
        phon_model = {}

    # save a list of all language codes used in this analysis
    o_name  = "Data/lang_codes" + identity + ".tsv"
    with open(o_name, 'w+', newline='') as f:
        write =  csv.writer(f, delimiter="\t")
        write.writerows(lang_codes)

    return None

if __name__ == "__main__": 
    main()