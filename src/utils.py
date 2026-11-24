from pathlib import Path
import pandas as pd


def load_df(p: str|Path, dedup=False, drop_hapax=False):

    df = pd.read_csv(p, sep="\t", index_col=0)

    subset = ["form", "pos", "feats", "lemma"]

    if drop_hapax:
        df = df[df.duplicated(subset=subset, keep=False)]

    if dedup:
        df = df.drop_duplicates(subset=subset)

    df = df[
        ~df["feats"].str.contains("Typo", na=False)
        & ~df["feats"].str.contains("Abbr", na=False)
        & ~df["feats"].str.contains("Anom", na=False)
    ]
    return df
