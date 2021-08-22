'''
Cleans PHOIBLE csv to just unique phonemes. 
'''

import pandas as pd 


def unique_csv(file_name):
    df = pd.read_csv(file_name)
    unique_df = df.drop_duplicates(subset=["Phoneme"])
    unique_df = unique_df.drop(labels=['InventoryID','Glottocode','ISO6393','LanguageName','SpecificDialect'], axis=1)
    unique_df.to_csv("data/phoible_unique_phonemes.csv", index=False)

unique_csv("data/phoible.csv")