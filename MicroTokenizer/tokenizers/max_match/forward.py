from typing import Dict, List

from MicroTokenizer import get_dict_file
from MicroTokenizer.data_structures.dictionary import DictionaryData
from MicroTokenizer.data_structures.train_dictionary import TrainDictionary
from MicroTokenizer.data_structures.trie_algorithm import TrieAlgorithm
from MicroTokenizer.tokenizers import BaseTokenizer


class MaxMatchForwardTokenizer(BaseTokenizer):
    def __init__(self, token_dict: Dict[str, int] = None) -> None:
        # for inference
        self.trie_tree = TrieAlgorithm(raw_dict_data=token_dict) if token_dict else None
        # for training
        self.token_dict = TrainDictionary()

    @classmethod
    def load(cls, model_dir: str):
        dict_file = get_dict_file(model_dir)
        token_dict = DictionaryData.read_dict(dict_file)
        return cls(token_dict)

    def save(self, model_dir: str):
        self.token_dict.persist_to_dir(model_dir)

    def train(self, corpus: List[List[str]]):
        for line in corpus:
            self.token_dict.train_one_line(line)
        self.token_dict.do_train()
        self.trie_tree = TrieAlgorithm(raw_dict_data = self.token_dict.dictionary)

    def segment(self, message: str) -> List[str]:
        token_result = []

        while message:
            max_match = None

            token_weight_pair = list(
                self.trie_tree.get_token_and_weight_at_text_head(message)
            )

            if token_weight_pair:
                # find the max long token
                sorted_token_weight_pair = sorted(
                    token_weight_pair, key=lambda x: len(x[0]), reverse=True
                )
                max_match = sorted_token_weight_pair[0][0]
            else:  # OOV now
                # use single character as token
                max_match = message[0]

            token_result.append(max_match)

            # update message, may cause while loop stop
            message = message[len(max_match) :]

        return token_result
