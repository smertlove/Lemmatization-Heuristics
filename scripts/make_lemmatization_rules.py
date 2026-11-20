from os.path import commonprefix
import attr
import json
from pathlib import Path
from tqdm import tqdm
from collections import defaultdict
from argparse import ArgumentParser
from src.utils import load_df
import pandas as pd
from src.structs import LemmatizeRule, WordForm



# from https://github.com/DanAnastasyev/GramEval2020/blob/master/solution/train/lemmatize_helper.py
def predict_lemmatize_rule(word: str, lemma: str):
    def _predict_lemmatize_rule(word: str, lemma: str, **kwargs):
        if len(word) == 0:
            return LemmatizeRule(append_suffix=lemma, **kwargs)

        common_prefix = commonprefix([word, lemma])
        if len(common_prefix) == 0:
            rule = _predict_lemmatize_rule(word[1:], lemma, **kwargs)
            return attr.evolve(rule, cut_prefix=rule.cut_prefix + 1)

        return LemmatizeRule(cut_suffix=len(word) - len(common_prefix),
                                append_suffix=lemma[len(common_prefix):], **kwargs)

    word, lemma = word.replace('ё', 'е'), lemma.replace('ё', 'е')
    return min([
        _predict_lemmatize_rule(word, lemma),
        _predict_lemmatize_rule(word.lower(), lemma, lower=True),
        _predict_lemmatize_rule(word.capitalize(), lemma, capitalize=True),
        _predict_lemmatize_rule(word.upper(), lemma, upper=True)
    ], key=lambda rule: rule.cut_prefix + rule.cut_suffix)



def _sort_rules(rules):
    return sorted(
        rules, key=lambda r: (
            r.cut_prefix, r.cut_suffix, r.append_suffix, r.lower, r.capitalize, r.upper
        )
    )


def main():

    parser = ArgumentParser()
    parser.add_argument("--data-path", type=str, required=True)
    parser.add_argument("--out-dir", type=str, required=True)

    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(exist_ok=True)
    id2rule_filename = out_dir / "id2rule.json"
    id2forms_filename = out_dir / "id2forms.json"
    assert not id2rule_filename.exists() and not id2forms_filename.exists()

    df = load_df(args.data_path, dedup=True)
    tqdm.pandas(desc="Подготовка правил лемматизации")
    df["lemmatization_rule"] = df.progress_apply(lambda row: predict_lemmatize_rule(row["form"], row["lemma"]), axis=1)
    unique_rules = df["lemmatization_rule"].unique()
    id2rule = {
        i: rule for i, rule
        in enumerate(_sort_rules(unique_rules))
    }
    rule2id = {rule: i for i, rule in id2rule.items()}
    df["rule_id"] = df["lemmatization_rule"].map(rule2id)

    id2wordforms = defaultdict(set)
    for rule_name, rule_group in df.groupby("rule_id"):
        for _, row in rule_group.iterrows():
            wf = WordForm.from_df_row(row)
            id2wordforms[rule_name].add(wf)

    
    with open(id2rule_filename, "w", encoding="utf-8") as file:
        json.dump({i: rule.to_dict() for i, rule in id2rule.items()},file, ensure_ascii=False, indent=2)

    with open(id2forms_filename, "w", encoding="utf-8") as file:
        json.dump({i: [form.to_dict() for form in forms] for i, forms in id2wordforms.items()},file, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
