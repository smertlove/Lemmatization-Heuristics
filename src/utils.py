from pathlib import Path
import pandas as pd


def load_df(p: str|Path, dedup=False):

    df = pd.read_csv(p, sep="\t", index_col=0)

    if dedup:
        df = df.drop_duplicates(subset=["form", "pos", "feats", "lemma"])

    df = df[
        ~df["feats"].str.contains("Typo", na=False)
        & ~df["feats"].str.contains("Abbr", na=False)
        & ~df["feats"].str.contains("Anom", na=False)
    ]
    return df
