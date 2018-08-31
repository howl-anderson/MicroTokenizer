# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from MicroTokenizer.DAG.dictionary.dictionary import DictionaryData


class HashTableAlgorithm(DictionaryData):
    def __init__(self, dict_file):
        super(HashTableAlgorithm, self).__init__(dict_file)

    def get_token_and_weight_at_text_head(self, text):
        for token, weight in self.dict_data.items():
            if text.startswith(token):
                yield token, weight

    def add_token_and_weight(self, token, weight):
        if token in self.dict_data:
            raise ValueError("token: {} already in dict_data".format(token))

        self.dict_data[token] = weight


if __name__ == "__main__":
    from timer_cm import Timer

    from MicroTokenizer import default_model_dir, get_dict_file

    dictionary_object = HashTableAlgorithm(get_dict_file(default_model_dir))

    with Timer('Building DAG graph'):
        for _ in range(100):
            result = list(
                dictionary_object.get_token_and_weight_at_text_head("王小明在北京的清华大学读书。")
            )

    print(result)
