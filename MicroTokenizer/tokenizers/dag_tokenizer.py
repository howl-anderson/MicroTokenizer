from typing import Dict, List

from MicroTokenizer import get_dict_file
from MicroTokenizer.data_structures.dictionary import DictionaryData
from MicroTokenizer.data_structures.non_recursive_algorithm import NonRecursiveAlgorithm
from MicroTokenizer.data_structures.train_dictionary import TrainDictionary
from MicroTokenizer.data_structures.trie_algorithm import TrieAlgorithm
from MicroTokenizer.tokenizers.base_tokenizer import BaseTokenizer


class DAGTokenizer(BaseTokenizer):
    def __init__(self, token_dict: Dict[str, int] = None):
        # for inference
        self.trie_tree = TrieAlgorithm(raw_dict_data=token_dict) if token_dict else None
        self.graph_builder = (
            NonRecursiveAlgorithm(self.trie_tree) if token_dict else None
        )
        # for training
        self.token_dict = TrainDictionary()

    @classmethod
    def load(cls, model_dir: str):
        dict_file = get_dict_file(model_dir)
        token_dict = DictionaryData.read_dict(dict_file)

        return cls(token_dict)

    def segment(self, message: str) -> List[str]:
        self.graph_builder.init_graph()
        self.graph_builder.build_graph(message)

        self.graph_builder.compute_shortest_path()

        raw_token = self.graph_builder.get_tokens()

        # remove start and end token
        return raw_token[1:-1]

    def train(self, corpus):
        for line in corpus:
            self.token_dict.train_one_line(line)
        self.token_dict.do_train()

        # load the new mode
        self.trie_tree = TrieAlgorithm(raw_dict_data=self.token_dict.dictionary)

        self.graph_builder = NonRecursiveAlgorithm(self.trie_tree)

    def save(self, output_dir: str):
        self.token_dict.persist_to_dir(output_dir)
