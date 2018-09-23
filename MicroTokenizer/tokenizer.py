from MicroTokenizer import default_model_dir
from MicroTokenizer.CRF.crf_tokenizer import CRFTokenizer
from MicroTokenizer.dag import DAGTokenizer
from MicroTokenizer.hmm import HMMTokenizer
from MicroTokenizer.max_match.backward import MaxMatchBackwardTokenizer
from MicroTokenizer.max_match.bidirectional import \
    MaxMatchBidirectionalTokenizer
from MicroTokenizer.max_match.forward import MaxMatchForwardTokenizer
from MicroTokenizer.merge_token import MergeSolutions


class Tokenizer(object):
    def __init__(self, model_dir=None):
        if model_dir is None:
            model_dir = default_model_dir

        self.model_dir = model_dir

        self.dag_tokenizer = None  # type: DAGTokenizer
        self.hmm_tokenizer = None  # type: HMMTokenizer
        self.max_match_forward_tokenizer = None  # type: MaxMatchForwardTokenizer
        self.max_match_backward_tokenizer = None  # type: MaxMatchBackwardTokenizer
        self.max_match_bidirectional_tokenizer = None  # type: MaxMatchBidirectionalTokenizer
        self.crf_tokenizer = None  # type: CRFTokenizer

    def init_dag_tokenizer(self):
        if self.dag_tokenizer is None:
            self.dag_tokenizer = DAGTokenizer(self.model_dir)
            self.dag_tokenizer.load_model()

    def cut_by_DAG(self, message):
        self.init_dag_tokenizer()
        return self.dag_tokenizer.segment(message)

    def init_hmm_tokenizer(self):
        if self.hmm_tokenizer is None:
            self.hmm_tokenizer = HMMTokenizer(self.model_dir)
            self.hmm_tokenizer.load_model()

    def cut_by_HMM(self, message):
        self.init_hmm_tokenizer()
        return self.hmm_tokenizer.segment(message)

    def cut_by_joint_model(self, message):
        solutions = [
            self.cut_by_DAG(message),
            self.cut_by_HMM(message)
        ]
        merge_solutions = MergeSolutions()
        best_solution = merge_solutions.merge(solutions)

        return best_solution

    def joint_solutions(self, solutions):
        merge_solutions = MergeSolutions()
        best_solution = merge_solutions.merge(solutions)

        return best_solution

    cut = cut_by_DAG

    def init_max_match_forward_tokenizer(self):
        if self.max_match_forward_tokenizer is None:
            self.max_match_forward_tokenizer = MaxMatchForwardTokenizer()
            self.max_match_forward_tokenizer.load_model()

    def cut_by_max_match_forward(self, message):
        self.init_max_match_forward_tokenizer()
        return self.max_match_forward_tokenizer.segment(message)

    def init_max_match_backward_tokenizer(self):
        if self.max_match_backward_tokenizer is None:
            self.max_match_backward_tokenizer = MaxMatchBackwardTokenizer()
            self.max_match_backward_tokenizer.load_model()

    def cut_by_max_match_backward(self, message):
        self.init_max_match_backward_tokenizer()
        return self.max_match_backward_tokenizer.segment(message)

    def init_max_match_bidirectional_tokenizer(self):
        if self.max_match_bidirectional_tokenizer is None:
            self.max_match_bidirectional_tokenizer = MaxMatchBidirectionalTokenizer()
            self.max_match_bidirectional_tokenizer.load_model()

    def cut_by_max_match_bidirectional(self, message):
        self.init_max_match_bidirectional_tokenizer()
        return self.max_match_bidirectional_tokenizer.segment(message)

    def init_crf_tokenizer(self):
        if self.crf_tokenizer is None:
            self.crf_tokenizer = CRFTokenizer()
            self.crf_tokenizer.load_model()

    def cut_by_CRF(self, message):
        self.init_crf_tokenizer()
        return self.crf_tokenizer.segment(message)

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
