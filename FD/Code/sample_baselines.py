import pandas as pd 
import os 
import json
import csv
from collections import defaultdict

NUM_SAMPLES = 1000 # number of artificial baselines per natural language

def main():
    word_lists = []
    identity ='5000_3' 
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
    
    progress = ''
    for i in range(len(split_list)):
        progress = progress + '-'
    progress = progress + ']'
    progress1 = '[|'
    progress = progress[1:]

    for lang in split_list:
        print(lang)
        natural_lexicon = split_list[lang]

        # getting only words that match generated words in length (3-8 segments)
        # we're gonna generate artificial baselines that have as many words as this filtered lexicon
        filtered_lexicon = list(filter(lambda x: 3 <= len(x.split(" ")) <= 8, natural_lexicon))
        # max = 0
        # for f in filtered_lexicon:
        #     f2 = filtered_lexicon.split(" ")
        #     if len(f2) > max: 
        #         print(f2)
        #         max = len(f2)
        all_words = {}
        with open("./Data/generated_words/" + lang + "_generated_words.json", 'r', encoding='utf8') as fin:
            all_words = json.load(fin)

        df = pd.DataFrame({'word': list(all_words.keys()), 
                           'prob': list(all_words.values())})

        progress = ''
        for i in range(NUM_SAMPLES):
            progress = progress + '-'
        progress = progress + ']'
        progress1 = '[|'
        progress = progress[1:]
        for i in range(1, NUM_SAMPLES + 1):
            print(progress1 + progress)
            progress1 =  progress1 +'|'
            progress = progress[1:]
            baseline = df["word"].sample(min(len(filtered_lexicon), len(df)), replace=False, weights=df["prob"]).tolist()

            if not os.path.exists('./Data/artificial_baselines'):
                os.makedirs('./Data/artificial_baselines')
            
            if not os.path.exists('./Data/artificial_baselines/' + lang):
                os.makedirs('./Data/artificial_baselines/' + lang)
            
            with open('./Data/artificial_baselines/' + lang + "/" + lang + "_baseline_" + str(i) + ".tsv", 'w', encoding='utf8', newline='') as fout:
                write =  csv.writer(fout, delimiter="\t")
                for word in baseline:
                    write.writerow([word])


if __name__ == "__main__":
    main()