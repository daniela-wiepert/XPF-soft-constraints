import pandas as pd 

df = pd.read_csv("percentiles.csv")
df = df.drop('Unnamed: 0', axis=1)

# drop langs with no fricatives
df = df[df["code"] != 'usa']
df = df[df["code"] != 'wbp']

# languages that are on the left for fricatives
fricatives_left = df[df['multiple_diff_fricatives'] < 0.5]
with open('langs_on_left_side_different.txt', 'w') as fout:
    for code in list(fricatives_left['code']):
        fout.write(code)
        fout.write("\n")

# langs that are on the right for fricatives
fricatives_right = df[df['multiple_diff_fricatives'] >= 0.5]
with open('langs_on_right_side_different.txt', 'w') as fout:
    for code in list(fricatives_right['code']):
        fout.write(code)
        fout.write("\n")

# langs where fricatives and sibilants don't match
# mismatched = df[abs(df['multiple_fricatives'] - df['multiple_sibilants']) >= 0.3]
# with open('langs_mismatched.txt', 'w') as fout:
#     for code in list(mismatched['code']):
#         fout.write(code)
#         fout.write("\n")


