import pandas as pd 
import csv

#TODO : change this
xpf_df = pd.read_csv('Data/langs-list-03.tsv', sep='\t')

#TODO: update this
identity='5000_3'
with open("Data/filtered_codes"+identity+".tsv", 'r') as fin:
    reader = csv.reader(fin, delimiter='\t')
    lang_codes = list(reader)
with open("Data/lang_codes.tsv", 'r') as fin:
    reader = csv.reader(fin, delimiter=' ')
    lang_codes2 = list(reader)

lang_codes2 = lang_codes2[1:]

for i in range(len(lang_codes)):
    lang_codes[i] = ''.join(lang_codes[i])

for i in range(len(lang_codes2)):
    h = lang_codes2[i][0].split(",")
    h = h[0]
    lang_codes2[i] = h

for code in lang_codes2:
    if not code in lang_codes:
        lang_codes.append(code)
# fd1 = ['acf', 'az', 'ba', 'be', 'bg', 'btx', 'bzh' 'ca', 'chm','cs','dyo','es','eu','hsb','hu','id','kbd','kea','kk','ky','ml','mt','myv','shi','sk','sq','tg','tr','tt','tzm','ug','uz','vi','wo','zza']

# for code in lang_codes2:
#     code = ''.join(code)
#     if not code in fd1:
#         fd1.append(code)
# with open('lang_codes.tsv', 'w') as fout:
#     writer = csv.writer(fout, delimiter='\t')
#     for code in ocp:
#         writer.writerow([code])

# quit()

# fd_df = xpf_df[xpf_df["code"].isin(fd)]
# fd_df = fd_df[["code", "name", "family"]]

# ocp_df = xpf_df[xpf_df["code"].isin(ocp)]
# ocp_df = ocp_df[["code", "name", "family"]]

# fd_df.to_csv('fd_languages.csv')
# ocp_df.to_csv('ocp_languages.csv')

df = xpf_df[xpf_df["code"].isin(lang_codes)]
df = df.sort_values(by='code', inplace=False)
df = df[["code","name","family"]]
df.to_csv("Data/all_lang_codes.csv", encoding='utf8')

