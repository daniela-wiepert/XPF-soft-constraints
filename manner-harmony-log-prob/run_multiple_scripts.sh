# mkdir data
# mkdir word_lists
# mkdir utf8_ngram_models
# mkdir generated_words
# mkdir artificial_baselines
# mkdir distributions
# mkdir visualizations

# python3 unique_phoible.py
# python3 all_counts02.py
# python3 ngram_model.py
python3 generate_lexicon.py
python3 sample_baselines.py
python3 count_ocp_violations_fast.py
# Manually delete usa and wbp from lang_codes.tsv, because they don't have fricatives
# run visualize.R in R (I don't have it set up in my terminal, which is why this is commented out)
# run percentile_medians.R
# python3 why_are_languages_extreme.py # you have to replace the file names depending on which type of co-occurrence you're looking at

### These were some sanity checks, not part of main pipeline ###
mkdir phoneme_frequencies
mkdir frequency_plots
mkdir distributions_baseline_check

python3 compare_phoneme_frequencies.py 
python3 plot_phoneme_frequencies.py

