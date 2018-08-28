from MicroTokenizer import default_model_dir, get_dict_file, get_crf_file
from MicroTokenizer.DAG.dictionary.trie_algorithm import TrieAlgorithm
from MicroTokenizer.dag import DAGTokenizer
from MicroTokenizer.hmm import HMMTokenizer
from MicroTokenizer.max_match.backward import MaxMatchBackwardTokenizer
from MicroTokenizer.max_match.forward import MaxMatchForwardTokenizer
from MicroTokenizer.max_match.bidirectional import MaxMatchBidirectionalTokenizer
from MicroTokenizer.CRF.crf_tokenizer import CRFTokenizer
from MicroTokenizer.merge_token import MergeSolutions


class Tokenizer(object):
    def __init__(self, model_dir=None):
        if model_dir is None:
            model_dir = default_model_dir

        self.model_dir = model_dir

        self.dict_data = self.load_data(self.model_dir)
        self.reversed_dict_data = self.load_reversed_data(self.model_dir)

        self.dag_tokenizer = DAGTokenizer(self.dict_data)  # type: DAGTokenizer

        self.hmm_tokenizer = HMMTokenizer.load_model(self.model_dir)

        self.max_match_forward_tokenizer = MaxMatchForwardTokenizer(
            self.dict_data)
        self.max_match_backward_tokenizer = MaxMatchBackwardTokenizer(
            self.reversed_dict_data)

        self.max_match_bidirectional_tokenizer = MaxMatchBidirectionalTokenizer(
            self.dict_data,
            self.reversed_dict_data
        )

        crf_file = get_crf_file(self.model_dir)
        self.crf_tokenizer = CRFTokenizer(crf_file)

    @staticmethod
    def load_data(model_dir):
        dag_dict_file = get_dict_file(model_dir)

        dict_data = TrieAlgorithm(dag_dict_file)

        return dict_data

    @staticmethod
    def load_reversed_data(model_dir):
        dag_dict_file = get_dict_file(model_dir)

        dict_data = TrieAlgorithm(dag_dict_file, reverse=True)

        return dict_data

    def cut_by_DAG(self, message):
        # clean the graph, just in case
        self.dag_tokenizer.init_graph()

        self.dag_tokenizer.build_graph(message)
        self.dag_tokenizer.compute_shortest_path()

        graph_token = self.dag_tokenizer.get_tokens()

        # remove start & end node which is not part of message
        message_token = graph_token[1:-1]
        return message_token

    def cut_by_HMM(self, message):
        message_token = self.hmm_tokenizer.predict(message)
        return message_token

    def cut_by_joint_model(self, message):
        solutions = [
            self.cut_by_DAG(message),
            self.cut_by_HMM(message)
        ]
        merge_solutions = MergeSolutions()
        best_solution = merge_solutions.merge(solutions)

        return best_solution

    cut = cut_by_DAG

    def cut_by_max_match_forward(self, message):
        message_token = self.max_match_forward_tokenizer.process(message)

        return message_token

    def cut_by_max_match_backward(self, message):
        message_token = self.max_match_backward_tokenizer.process(message)

        return message_token

    def cut_by_max_match_bidirectional(self, message):
        message_token = self.max_match_bidirectional_tokenizer.process(message)

        return message_token

    def cut_by_CRF(self, message):
        message_token = self.crf_tokenizer.cut(message)

        return message_token

    def load_custom_dict(self, dict_file):
        # TODO: not implement yet
        pass

    def add_word(self, word, freq=None):
        # TODO: not implement yet
        pass

    def del_word(self, word):
        # TODO: not implement yet
        pass

    def load_user_dict(self, dict_file):
        return self.dag_tokenizer.dict_data.load_user_dict(dict_file)

    @property
    def mini_log_freq(self):
        # TODO: not implement yet
        pass

    @property
    def average_log_freq(self):
        # TODO: not implement yet
        pass


if __name__ == "__main__":
    tokenizer = Tokenizer()
    print(tokenizer.cut("王小明在北京的清华大学读书。"))
    print(tokenizer.cut_by_DAG("王小明在北京的清华大学读书。"))
    print(tokenizer.cut_by_HMM("王小明在北京的清华大学读书。"))
    print(tokenizer.cut_by_joint_model("王小明在北京的清华大学读书。"))
