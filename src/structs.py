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
