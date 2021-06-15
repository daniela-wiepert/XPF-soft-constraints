import pandas as pd 
import os 
import csv 
import matplotlib.pyplot as plt 
import json 
import math

lang_codes = []
with open("lang_codes.tsv", 'r') as fin:
    reader = csv.reader(fin, delimiter='\t')
    lang_codes = list(reader)

num_rows = 12
num_cols = 5
fig, axs = plt.subplots(num_rows, num_cols)
counter = 0
for lang_code in lang_codes: 
    lang_code = lang_code[0]
    print("lang code: ", lang_code)
    r = counter // num_cols
    c = counter - (r * num_cols)

    generated = {}
    natural = {}

    with open('biphone_frequencies/' + lang_code + '_generated_frequencies.json', 'r', encoding='utf8') as fin:
        generated = json.load(fin)

    with open('biphone_frequencies/' + lang_code + '_natural_frequencies.json', 'r', encoding='utf8') as fin:
        natural = json.load(fin)

    generated_log = {}
    for k, v in generated.items():
        generated_log[k] = math.log(v)

    natural_log = {}
    for k, v in natural.items():
        k = k.replace(" ː", "ː")
        natural_log[k] = math.log(v)

    natural_freqs = []
    generated_freqs = []
    labels = []
    for k, v in generated_log.items():
        if not natural_log.get(k) == None:
            generated_freqs.append(v)
            natural_freqs.append(natural_log.get(k))
            labels.append(k)

            if v - natural_log.get(k) > 1:
                print(k)

    axs[r, c].scatter(generated_freqs, natural_freqs)
    axs[r, c].set_title(lang_code + " phoneme frequencies (log-scale)")
    axs[r, c].set(xlabel="Generated", ylabel="Natural")

    # i = 0
    # for k in labels:
    #     axs[r, c].annotate(k, (generated_freqs[i], natural_freqs[i]), xytext=(3, 3), textcoords='offset points')
    #     i += 1
    counter += 1

figure = plt.gcf()
figure.set_size_inches(20, 48)
plt.tight_layout()
plt.savefig("frequency_plots/biphone_all_subplots.png")
