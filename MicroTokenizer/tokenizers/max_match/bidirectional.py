import operator

from MicroTokenizer.tokenizers import BaseTokenizer
from MicroTokenizer.tokenizers.max_match.backward import MaxMatchBackwardTokenizer
from MicroTokenizer.tokenizers.max_match.forward import MaxMatchForwardTokenizer


class MaxMatchBidirectionalTokenizer(BaseTokenizer):
    def __init__(self, forward_tokenizer=None, backward_tokenizer=None):
        self.forward_tokenizer = forward_tokenizer
        self.backward_tokenizer = backward_tokenizer

    def train(self, corpus):
        self.forward_tokenizer = MaxMatchForwardTokenizer()
        self.forward_tokenizer.train(corpus)

        self.backward_tokenizer = MaxMatchBackwardTokenizer()
        self.backward_tokenizer.train(corpus)

    @classmethod
    def load(cls, model_dir):
        forward_tokenizer = MaxMatchForwardTokenizer.load(model_dir)
        backward_tokenizer = MaxMatchBackwardTokenizer.load(model_dir)

        return cls(forward_tokenizer, backward_tokenizer)

    def save(self, model_dir: str):
        self.forward_tokenizer.save(model_dir)
        self.backward_tokenizer.save(model_dir)

    def segment(self, message):
        forward_token = self.forward_tokenizer.segment(message)
        backward_token = self.backward_tokenizer.segment(message)

        token_result = [forward_token, backward_token]

        token_count = operator.le(*map(self.compute_token_count, token_result))

        token_granularity = operator.ge(
            *map(self.compute_token_granularity, token_result)
        )

        token_len_variability = operator.le(
            *map(self.compute_token_len_variability, token_result)
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
        return sum(map(lambda x: abs(len(x) - mean_length) ** 2, token_list)) / len(
            token_list
        )
