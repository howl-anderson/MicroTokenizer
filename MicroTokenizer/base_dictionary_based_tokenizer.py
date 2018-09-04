from typing import List, Dict

from MicroTokenizer import get_dict_file
from MicroTokenizer.DAG.dictionary.dictionary import DictionaryData
from MicroTokenizer.DAG.graph_builder.graph_builder import GraphBuilder
from MicroTokenizer.base_tokenizer import BaseTokenizer
from MicroTokenizer.DAG.dictionary.train_dictionary import TrainDictionary


class BaseDictionaryBasedTokenizer(BaseTokenizer):
    def __init__(self, *args, **kwargs):
        super(BaseDictionaryBasedTokenizer, self).__init__(*args, **kwargs)

        self.train_dictionary = TrainDictionary()
        self.dict_data = kwargs.get('dict_data')  # type: DictionaryData
        self.dict_file = None  # type: str
        self.raw_dict_data = None  # type: Dict

    def load_model(self):
        self.dict_file = get_dict_file(self.model_dir)

    def segment(self, message):
        # type: (str) -> List[str]
        raise NotImplemented

    def train_one_line(self, token_list):
        # type: (List[str]) -> None
        self.train_dictionary.train_one_line(token_list)

    def do_train(self):
        self.train_dictionary.do_train()

        self.raw_dict_data = self.train_dictionary.dictionary

    def persist_to_dir(self, output_dir):
        # type: (str) -> None
        self.train_dictionary.persist_to_dir(output_dir)

    def assign_from_loader(self, *args, **kwargs):
        self.dict_file = kwargs['dict_file']
        self.dict_data = kwargs['dict_data']
