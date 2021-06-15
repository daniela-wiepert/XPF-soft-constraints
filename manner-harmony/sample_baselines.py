import pandas as pd 
import os 
import json
import csv
from collections import defaultdict

NUM_SAMPLES = 1000 # number of artificial baselines per natural language

def main(n=3, wordlen=10):
    lang_codes = []
    with open("lang_codes.tsv", 'r') as fin:
        reader = csv.reader(fin, delimiter='\t')
        lang_codes = list(reader)
    
    for lang_code in lang_codes:
        lang_code = lang_code[0]
        print("lang_code: ", lang_code)

        # Get 5000 most frequent words from natural language, plus all the words at the same final frequency
        # the natural lexicon is already the 5000 most frequent along with the extra words at the last frequency
        natural_lexicon = []
        with open("word_lists/" + lang_code + '_word_list.tsv', 'r', encoding='utf8') as fin:
            reader = csv.reader(fin, delimiter='\t')
            natural_lexicon = list(reader)

        # getting only words that match generated words in length (num of segments)
        # we're gonna generate artificial baselines that have as many words as this filtered lexicon
        filtered_lexicon = list(filter(lambda x: n-1 <= len(x[0].split(" ")) <= wordlen-2, natural_lexicon))

        all_words = {}
        with open("generated_words/" + lang_code + "_generated_words.json", 'r', encoding='utf8') as fin:
            all_words = json.load(fin)

        # df = pd.DataFrame.from_records(all_words, index=list(range(len(all_words.keys()))))
        df = pd.DataFrame({'word': list(all_words.keys()), 
                           'prob': list(all_words.values())})

        for i in range(1, NUM_SAMPLES + 1):
            baseline = df["word"].sample(min(len(filtered_lexicon), len(df)), replace=False, weights=df["prob"]).tolist()

            if not os.path.exists('artificial_baselines'):
                os.makedirs('artificial_baselines')
            
            if not os.path.exists('artificial_baselines/' + lang_code):
                os.makedirs('artificial_baselines/' + lang_code)
            
            with open('artificial_baselines/' + lang_code + "/" + lang_code + "_baseline_" + str(i) + ".tsv", 'w', encoding='utf8', newline='') as fout:
                write =  csv.writer(fout, delimiter="\t")
                for word in baseline:
                    write.writerow([word])


if __name__ == "__main__":
    main()