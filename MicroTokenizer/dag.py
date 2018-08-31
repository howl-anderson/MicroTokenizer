from typing import List

from MicroTokenizer import get_dict_file
from MicroTokenizer.DAG.dictionary.dictionary import DictionaryData
from MicroTokenizer.DAG.dictionary.trie_algorithm import TrieAlgorithm
from MicroTokenizer.DAG.graph_builder.graph_builder import GraphBuilder
from MicroTokenizer.DAG.graph_builder.non_recursive_algorithm import NonRecursiveAlgorithm
from MicroTokenizer.base_tokenizer import BaseTokenizer
from MicroTokenizer.DAG.dictionary.train_dictionary import TrainDictionary


class DAGTokenizer(BaseTokenizer):
    def __init__(self, *args, **kwargs):
        super(DAGTokenizer, self).__init__(*args, **kwargs)

        self.graph_builder = None  # type: GraphBuilder
        self.train_dictionary = TrainDictionary()
        self.dict_data = None  # type: DictionaryData

    def load_model(self):
        dag_dict_file = get_dict_file(self.model_dir)

        self.dict_data = TrieAlgorithm(dag_dict_file)

        self.graph_builder = NonRecursiveAlgorithm(self.dict_data)

    def segment(self, message):
        # type: (str) -> List[str]

        self.graph_builder.init_graph()
        self.graph_builder.build_graph(message)

        self.graph_builder.compute_shortest_path()

        raw_token = self.graph_builder.get_tokens()

        # remove start and end token
        return raw_token[1:-1]

    def train_one_line(self, token_list):
        # type: (List[str]) -> None

        self.train_dictionary.train_one_line(token_list)

    def do_train(self):
        self.train_dictionary.do_train()

        # load the new model
        self.dict_data = TrieAlgorithm(raw_dict_data=self.train_dictionary.dictionary)

        self.graph_builder = NonRecursiveAlgorithm(self.dict_data)

    def persist_to_dir(self, output_dir):
        # type: (str) -> None

        self.train_dictionary.persist_to_dir(output_dir)
