import pandas as pd 
import os 
import csv 
import matplotlib.pyplot as plt 
import json 
import math


lang_codes = []
filtered_codes = []
filtered_codes2 = []
f1 = []
f2 = []
f3 = []
f4 = []
identity = '5000_3'
with open("Data/lang_codes"+identity+".tsv", 'r') as fin:
    reader = csv.reader(fin, delimiter='\t')
    lang_codes = list(reader)

# with open("Data/filtered_codes"+identity+".tsv", 'r') as fin:
#     reader = csv.reader(fin, delimiter='\t')
#     f_codes = list(reader)
# filtered = []
# for code in f_codes:
#     c = ''.join(code)
#     filtered.append(c)

phoneme_features = pd.read_csv("Data/resolved-phoible.csv")
phoneme_features.drop(["InventoryID", "Glottocode","ISO6393","LanguageName","SpecificDialect","GlyphID","Allophones","Marginal","Source"], axis="columns", inplace=True)
phoneme_features = phoneme_features.rename(columns={'periodicGlottalSource':'voice'})
features = phoneme_features.copy()
features.drop(["Phoneme","voice"],axis="columns", inplace=True)
features = features.columns.values.tolist()


count = 0

for lang_code in lang_codes: 
    lang_code = ''.join(lang_code)
    print(lang_code)
    
    voiced = 0
    voiceless = 0
    any_final = 0
    any_initial = 0 
    obs_final = 0
    obs_initial = 0
    with open('./Data/phoneme_frequencies/' + lang_code + '_natural_counts_final.json', 'r', encoding='utf8') as fin:
        natural = json.load(fin)
    with open('Data/phoneme_frequencies/' + lang_code + '_natural_counts_initial.json', 'r', encoding='utf8') as fin:
        natural2 = json.load(fin)
    with open('Data/phoneme_frequencies/' + lang_code + '_natural_counts.json', 'r', encoding='utf8') as fin:
        natural3 = json.load(fin)
    
    # if lang_code in filtered:
    with open('Data/distributions/' + lang_code + '_natural.csv','r') as fin:
        reader = csv.reader(fin, delimiter='\t')
        natural_dist = list(reader)
        natural_dist = float(natural_dist[1][0])
    # else: 
    #     natural_dist = 0.0
    
    for k,v in natural.items():
        row = phoneme_features[phoneme_features["Phoneme"] == k]
        if not row.empty:
            if row["SegmentClass"].tolist()[0] == "consonant":
                any_final += v
 
    for k,v in natural2.items():
        row = phoneme_features[phoneme_features["Phoneme"] == k]
        if not row.empty:
            if row["SegmentClass"].tolist()[0] == "consonant":
                any_initial += v
    
    for k,v in natural3.items():
        row = phoneme_features[phoneme_features["Phoneme"] == k]
        if not row.empty:
            if row["SegmentClass"].tolist()[0] == "consonant":
                if row["sonorant"].tolist()[0] == '-':
                    if row["voice"].tolist()[0] == "+":
                        voiced += v 
                    elif row["voice"].tolist()[0] == "-":
                        voiceless += v
  
    if any_final != 0  and  any_initial != 0:
        if math.log(any_final/any_initial) < 0:
            f1.append(lang_code)
    
    if natural_dist > 0.02:
        f2.append(lang_code)

    if voiceless != 0 and voiced != 0:
        if math.log(voiceless/voiced) > 0:
            f3.append(lang_code)

for lang_code in lang_codes:
    lang_code = ''.join(lang_code)
    if lang_code in f1  and lang_code in f2 and lang_code in f3:
        filtered_codes.append(lang_code)

print(len(filtered_codes))
print(filtered_codes)

o_name  = "./Data/filtered_codes" + identity + ".tsv"
with open(o_name, 'w+', newline='') as f:
    write =  csv.writer(f, delimiter="\t")
    write.writerows(filtered_codes)