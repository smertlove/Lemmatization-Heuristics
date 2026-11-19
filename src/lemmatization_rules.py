from os.path import commonprefix
import attr
import json


@attr.s(frozen=True)
class LemmatizeRule(object):
    cut_prefix = attr.ib(default=0)
    cut_suffix = attr.ib(default=0)
    append_suffix = attr.ib(default='')
    lower = attr.ib(default=False)
    capitalize = attr.ib(default=False)
    upper = attr.ib(default=False)

    def to_json(self):
        return json.dumps(self.__dict__, ensure_ascii=False)


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
