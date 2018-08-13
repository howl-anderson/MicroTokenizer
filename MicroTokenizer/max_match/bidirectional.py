import operator

from MicroTokenizer.max_match.forward import MaxMatchForwardTokenizer
from MicroTokenizer.max_match.backward import MaxMatchBackwardTokenizer


class MaxMatchBidirectionalTokenizer(object):
    def __init__(self, dict_data, reverse_dict_data):
        self.forward_tokenizer = MaxMatchForwardTokenizer(dict_data)
        self.backward_tokenizer = MaxMatchBackwardTokenizer(reverse_dict_data)

    def process(self, message):
        forward_token = self.forward_tokenizer.process(message)
        backward_token = self.backward_tokenizer.process(message)

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


if __name__ == "__main__":
    from MicroTokenizer import default_model_dir, get_dict_file
    from MicroTokenizer.DAG.dictionary.trie_algorithm import TrieAlgorithm

    dag_dict_file = get_dict_file(default_model_dir)

    dict_data = TrieAlgorithm(dag_dict_file)
    reversed_dict_data = TrieAlgorithm(dag_dict_file, reverse=True)

    tokenizer = MaxMatchBidirectionalTokenizer(dict_data, reversed_dict_data)

    result = tokenizer.process("中国的首都是北京")
    print(result)

    result = tokenizer.process("我们在野生动物园玩")
    print(result)

    result = tokenizer.process("王小明在北京的清华大学读书。")
    print(result)
