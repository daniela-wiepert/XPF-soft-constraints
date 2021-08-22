# manner-harmony
Up-to-date as of: June 15, 2021

As a note, these files were written when we were studying both fricatives generally and sibilants specifically, so you will see some code related to sibilants only. You can ignore this. 

## Before you run
For any script, you may need to change internal file name variables in order to access XPF directory files or set working directories.

You will also need to get Crubadan wordlists and XPF rules from [Dropbox](https://www.dropbox.com/sh/pb8pqsl9cutl66g/AACRVzaJTekQoGMaGKqQ6m9za?dl=0). 

## Running it on your own
Follow the instructions in `run_multiple_scripts.sh`.

## Description of scripts
All files are written by Rebecca Mathew. Scripts are presented in the order needed to run. 

- `unique_phoible.py`: Pares down [the raw PHOIBLE data](https://github.com/phoible/dev/blob/master/data/phoible.csv) to having unique phonemes. 
- `all_counts02.py`: Gets the IPA forms for the top ~5000 most frequent types for usable natural languages. This file uses `wordseg.py`. Outputs to `word_lists` directory
- `ngram_models.py`: Creates 4-gram models. Outputs to `utf8_ngram_models` directory
- `generate_lexicon.py`: Creates all possible words with their probability of occurring from the n-gram models. Outputs to `generated_words` directory
- `sample_baselines.py`: Samples from the generated words to create baselines. Outputs to `artificial_baselines`
- `count_ocp_violations_fast.py`: Gets percent of violations for various OCP hypotheses for the natural and baseline languages. Outputs to `distributions`
- `visualize.R`: Calculates percentiles and creates density plots of comparing natural languages to baselines. Outputs to this directory. Also creates `percentiles.csv` and outputs CSVs of significant individual languages. 
- `percentiles_median.R`: Used for finding medians from `percentiles.csv`
- `why_are_languages_extreme.py`: Identifies which languages are in the bottom half of percentiles and which are in the top half.
- `compare_phoneme_frequencies.py`: Used for sanity checks. Getting uniphone frequencies for natural and generated lexicons. Outputs to `phoneme_frequencies` directory
- `compare_biphone_frequencies.py`: Same as above, but for biphones.
- `plot_phoneme_frequencies.py`: Used for sanity checks. The commented out section (multi-line string) creates individual language plots. The bottom section creates a grid of individual plots of the natural vs generate phoneme log-frequencies for each language. Outputs to `frequency_plots` directory
- `plot_biphone_frequencies.py`: Same as above, but for biphones.
- `example_oe_diagram.R`: The script we used to create the made-up vowel harmony diagram in the paper. 