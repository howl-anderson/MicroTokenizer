import operator

from MicroTokenizer.DAG.dictionary.trie_algorithm import TrieAlgorithm
from MicroTokenizer.base_dictionary_based_tokenizer import \
    BaseDictionaryBasedTokenizer
from MicroTokenizer.bidirectional_dictionary_loader import \
    BidirectionalDictionaryBasedLoader
from MicroTokenizer.max_match.backward import MaxMatchBackwardTokenizer
from MicroTokenizer.max_match.forward import MaxMatchForwardTokenizer


class MaxMatchBidirectionalTokenizer(BaseDictionaryBasedTokenizer):
    def __init__(self, *args, **kwargs):
        super(MaxMatchBidirectionalTokenizer, self).__init__(*args, **kwargs)

        self.forward_tokenizer = None
        self.backward_tokenizer = None

    def do_train(self):
        super(MaxMatchBidirectionalTokenizer, self).do_train()

        dict_data = TrieAlgorithm(raw_dict_data=self.raw_dict_data)

        reverse_dict_data = TrieAlgorithm(raw_dict_data=self.raw_dict_data,
                                          reverse=True)

        self.forward_tokenizer = MaxMatchForwardTokenizer(dict_data=dict_data)

        self.backward_tokenizer = MaxMatchBackwardTokenizer(dict_data=reverse_dict_data)

    def load_model(self):
        super(MaxMatchBidirectionalTokenizer, self).load_model()

        self.forward_tokenizer = MaxMatchForwardTokenizer(self.model_dir)
        self.forward_tokenizer.load_model()

        self.backward_tokenizer = MaxMatchBackwardTokenizer(self.model_dir)
        self.backward_tokenizer.load_model()

    def segment(self, message):
        forward_token = self.forward_tokenizer.segment(message)
        backward_token = self.backward_tokenizer.segment(message)

        token_result = [forward_token, backward_token]

        token_count = operator.le(
            * map(self.compute_token_count, token_result)
        )

        token_granularity = operator.ge(
            * map(self.compute_token_granularity, token_result)
        )

        token_len_variability = operator.le(
            * map(self.compute_token_len_variability, token_result)
        )

        if token_count + token_granularity + token_len_variability >= 2:
            return forward_token
        else:
            return backward_token

    @staticmethod
    def compute_token_granularity(token_list):
        return sum(map(lambda x: len(x), token_list)) / len(token_list)

    @staticmethod
    def compute_token_oov_rate(token_list):
        # FIXME: method is_oov() is not exits yet
        return sum(map(lambda x: x.is_oov, token_list)) / len(token_list)

    @staticmethod
    def compute_token_count(token_list):
        return len(token_list)

    @staticmethod
    def compute_token_len_variability(token_list):
        mean_length = sum(map(lambda x: len(x), token_list)) / len(token_list)
        return sum(map(lambda x: abs(len(x) - mean_length)**2, token_list)) / len(token_list)

    def get_loader(self):
        return BidirectionalDictionaryBasedLoader

    def assign_from_loader(self, *args, **kwargs):
        self.forward_tokenizer = kwargs['forward_tokenizer']
        self.backward_tokenizer = kwargs['backward_tokenizer']
