from pathlib import Path
import pandas as pd
import json
from src.structs import WordForm, LemmatizeRule


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


def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data
    

def load_id2rule(path):
    data = load_json(path)
    data = {i: LemmatizeRule(**args) for i, args in data.items()}


def load_id2forms(path):
    data = load_json(path)
    data = {i: [WordForm(**args) for args in forms] for i, forms in data.items()}
