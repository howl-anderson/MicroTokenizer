"""Top-level package for Micro Tokenizer for Chinese."""
__version__ = "0.21.1"

import os

current_dir = os.path.dirname(os.path.abspath(__file__))

default_model_dir = os.path.join(current_dir, 'model_data')
current_model_dir = default_model_dir


def get_dict_file(model_dir):
    return os.path.join(model_dir, 'dict.txt')

from MicroTokenizer.tokenizers.max_match.backward import MaxMatchBackwardTokenizer
from MicroTokenizer.tokenizers.max_match.forward import MaxMatchForwardTokenizer
from MicroTokenizer.tokenizers.max_match.bidirectional import MaxMatchBidirectionalTokenizer
from MicroTokenizer.tokenizers.dag_tokenizer import DAGTokenizer
from MicroTokenizer.tokenizers.hmm_tokenizer import HMMTokenizer
from MicroTokenizer.tokenizers.crf.tokenizer import CRFTokenizer
from MicroTokenizer.ensemble.merge_solutions import MergeSolutions

max_match_backward_tokenizer = MaxMatchBackwardTokenizer.load(default_model_dir)
max_match_forward_tokenizer = MaxMatchForwardTokenizer.load(default_model_dir)
max_match_bidirectional_tokenizer = MaxMatchBidirectionalTokenizer.load(default_model_dir)
dag_tokenizer = DAGTokenizer.load(default_model_dir)
hmm_tokenizer = HMMTokenizer.load(default_model_dir)
crf_tokenizer = CRFTokenizer.load(default_model_dir)


def _cut_by_dag_hmm_joint_model(message):
    solutions = [
        dag_tokenizer.segment(message),
        hmm_tokenizer.segment(message)
    ]
    merge_solutions = MergeSolutions()
    best_solution = merge_solutions.merge(solutions)

    return best_solution

# this is a jieba (https://github.com/fxsjy/jieba) compatible API
def cut(message, HMM=False):
    if HMM:
        return _cut_by_dag_hmm_joint_model(message)
    else:
        return dag_tokenizer.segment(message)


# this is a jieba (https://github.com/fxsjy/jieba) compatible API
def load_userdict(dict_file):
    return dag_tokenizer.trie_tree.load_user_dict(dict_file)
