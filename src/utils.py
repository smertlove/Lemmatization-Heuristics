import pandas as pd
from pathlib import Path

def load_and_dedup_df(p: str|Path):
    df = pd.read_csv(p, sep="\t", index_col=0)
    df = df.drop_duplicates(subset=["form", "pos", "feats", "lemma"])
    # df = df[
    #     ~df["feats"].str.contains("Typo", na=False)
    #     & ~df["feats"].str.contains("Abbr", na=False)
    #     & ~df["feats"].str.contains("Anom", na=False)
    # ]
    return df

