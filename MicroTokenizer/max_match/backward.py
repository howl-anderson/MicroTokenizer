from typing import List

from MicroTokenizer.DAG.dictionary.trie_algorithm import TrieAlgorithm
from MicroTokenizer.backward_dictionary_loader import \
    BackwardDictionaryBasedLoader
from MicroTokenizer.base_dictionary_based_tokenizer import BaseDictionaryBasedTokenizer


class MaxMatchBackwardTokenizer(BaseDictionaryBasedTokenizer):
    def load_model(self):
        super(MaxMatchBackwardTokenizer, self).load_model()

        self.dict_data = TrieAlgorithm(self.dict_file, reverse=True)

    def do_train(self):
        super(MaxMatchBackwardTokenizer, self).do_train()

        self.dict_data = TrieAlgorithm(raw_dict_data=self.raw_dict_data, reverse=True)

    def segment(self, message):
        # type: (str) -> List[str]

        reversed_token_result = []

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
                max_match = message[-1]

            reversed_token_result.append(max_match)

            message = message[: - len(max_match)]

            if not message:
                # no more message
                break

        return list(reversed(reversed_token_result))

    def get_loader(self):
        return BackwardDictionaryBasedLoader
