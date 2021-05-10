# XPF-soft-constraints
# FINAL-OBSTRUENT DEVOICING 
UP TO DATE AS OF: 05/09/2021
List of project files/dependencies

** NOTE: for any .py script, you may need to change internal file name variables in order to access XPF directory files

1. resolve_phoible.R
      * this does not need to be run, but if there are any phonemes that are missing but have a close match, you can add the phoneme pair to this file to change the phoible phoneme to the one that matches the transcription. Phoible has some weird extra characters on the phonemes that can make matching impossible.

2. all_counts04.py
    * gets phonemic translations for words in all languages in the laguage list
    * can specify: language list (default: Code/langs-list-03.tsv)
                   arguments for stopatn - # types (default: 5000), cut-off frequency (default: 3)
    * file dependencies:
          access to XPF directory
          sumstats01.py
          translate04.py
          stopatn.sh
    * output: a tsv file containing language code and translated words (word_list.tsv)

3.  ngram_model_fd.py
    * originally written by Rebecca Mathew
    * modified by Daniela Wiepert
    * creates an ngram model (default n = 4)
    * file dependencies:
        word_list*.tsv (generated from all_counts04.py)
        resolved-phoible.csv (generated from resolve_phoible.R)
    * output: model, phon_model, to_feat    
        - model is a dictionary with the n-gram context (ie. '[_w a m i') as a key, and the value is another dictionary containing the phonemes that follow and the number of times they follow a given context. Changes any occurrences of obstruents appearing word-finally into a feature string containing all the features from phoible EXCEPT voicing information - so /k/ might change to 'consonant/SegmentClass|-/sonorant|-/continuant|....', whereas vowels and non-sonorants have perfect representations - /a/ = 'a', /m/ = 'm',  etc. Removing voicing information allows the model to generate lexicons with final voicing contrasts that occur with equal frequency. This current model does it any time it sees an obstruent, but this shouldn't cause an issue since if given a context with 'k a g', the model will generate a lexicon with 'g a k' 'g a g' 'k a k' 'k a g', so with many samples, it should balance? QUESTION THIS? An improvement may be to do this only for final contexts 'g a OBSTRUENT ]_w'
        - phon_model is a dictionary mapping a feature representation to another dictionary containing the phonemes that the feature corresponds with plus the number of occurrences of each phoneme
        - to_feat is a dictionary mapping phonemes to their corresponding feature representation
    
4. generate_lexicon_fd.py
    * originallywritten by Rebecca Mathew
    * modified by Daniela Wiepert
    * This code generates all possible words that can be created given contexts + phoneme representations + probabilites.
    * all combined probabilites are calculated as log probabilites

5. sample_baselines.py
    * written by Rebecca Mathew
    * adapted for final devoicing by Daniela Wiepert
    * This code samples the generated lexicons to produce 100 artificial baseline languages per natural language


6. compare_phoneme_frequencies.py
    * written by Rebecca Mathew
    * modified for final devoicing by Daniela Wiepert
    * gets counts of all phonemes in all positions in the natural and in the generated lexicon

7. compare_phoneme_frequences_initial.py

8. compare_phoneme_frequencies_final.py

9. filter_langs.py

10. plot_phoneme_frequencies.py
    * written by Rebecca Mathew
    * adapted for final devoicing by Daniela Wiepert

11. count_fd_violations.py 


12. visualize.Rmd
    * written by Rebecca Mathew
    * adapted for final devoicing by Daniela Wiepert


