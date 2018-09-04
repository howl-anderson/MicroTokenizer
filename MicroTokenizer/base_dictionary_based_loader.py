import os
from typing import List, Union

from MicroTokenizer.DAG.dictionary.trie_algorithm import TrieAlgorithm
from MicroTokenizer.base_loader import BaseLoader
from MicroTokenizer.base_tokenizer import BaseTokenizer


class BaseDictionaryBasedLoader(BaseLoader):
    def __init__(self, *args, **kwargs):
        super(BaseDictionaryBasedLoader, self).__init__(*args, **kwargs)

        self.dict_file = None
        self.dict_data = None

    def from_disk(self, model_path, tokenizer_list, reverse=False):
        # type: (Union[str, None], List[BaseTokenizer], bool) -> None

        if not self.dict_data:
            self.dict_file = self.get_dict_file(model_path)
            self.dict_data = TrieAlgorithm(self.dict_file, reverse=reverse)

        for tokenizer in tokenizer_list:
            tokenizer.assign_from_loader(dict_data=self.dict_data, dict_file=self.dict_file)

    @staticmethod
    def get_dict_file(model_dir):
        return os.path.join(str(model_dir), 'dict.txt')

    def get_model_dir(self):
        return 'dictionary_based'
