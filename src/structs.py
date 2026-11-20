import attr
import pandas as pd

# from https://github.com/DanAnastasyev/GramEval2020/blob/master/solution/train/lemmatize_helper.py
@attr.s(frozen=True)
class LemmatizeRule(object):
    cut_prefix = attr.ib(default=0)
    cut_suffix = attr.ib(default=0)
    append_suffix = attr.ib(default='')
    lower = attr.ib(default=False)
    capitalize = attr.ib(default=False)
    upper = attr.ib(default=False)

    def to_dict(self):
        return attr.asdict(self)


@attr.s(frozen=True)
class WordForm(object):
    form = attr.ib(default=None)
    lemma=attr.ib(default=None)
    pos=attr.ib(default=None)
    feats=attr.ib(default=None)

    def to_dict(self):
        return attr.asdict(self)

    @classmethod
    def from_df_row(cls, df_row):
        def clean(val):
            return None if pd.isna(val) else val

        return cls(
            form=clean(df_row["form"]),
            lemma=clean(df_row["lemma"]),
            pos=clean(df_row["pos"]),
            feats=clean(df_row["feats"]),
        )
