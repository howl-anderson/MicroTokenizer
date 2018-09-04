from typing import List

from MicroTokenizer.DAG.dictionary.trie_algorithm import TrieAlgorithm
from MicroTokenizer.base_dictionary_based_tokenizer import BaseDictionaryBasedTokenizer
from MicroTokenizer.forward_dictionary_loader import ForwardDictionaryBasedLoader


class MaxMatchForwardTokenizer(BaseDictionaryBasedTokenizer):
    def load_model(self):
        super(MaxMatchForwardTokenizer, self).load_model()

        self.dict_data = TrieAlgorithm(self.dict_file)

    def do_train(self):
        super(MaxMatchForwardTokenizer, self).do_train()

        self.dict_data = TrieAlgorithm(raw_dict_data=self.raw_dict_data)

    def segment(self, message):
        # type: (str) -> List[str]

        token_result = []

        while True:
            token_weight_pair = list(
                self.dict_data.get_token_and_weight_at_text_head(
                    message)
            )

            max_match = None

            if token_weight_pair:
                sorted_token_weight_pair = sorted(token_weight_pair,
                                                  key=lambda x: len(x[0]),
                                                  reverse=True)

                max_match = sorted_token_weight_pair[0][0]

            else:  # OOV now
                max_match = message[0]

            token_result.append(max_match)

            message = message[len(max_match):]

            if not message:
                # no more message
                break

        return token_result

    def get_loader(self):
        return ForwardDictionaryBasedLoader
