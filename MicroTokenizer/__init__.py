from .errors import Warnings, deprecation_warning

"""Top-level package for Micro Tokenizer for Chinese."""
import os

__author__ = """Xiaoquan Kong"""
__email__ = 'u1mail2me@gmail.com'
__version__ = ''
__long_description__ = ''

current_dir = os.path.dirname(os.path.abspath(__file__))

# dynamic load version from version file
version_file = os.path.join(current_dir, 'version.txt')
with open(version_file, encoding="utf-8") as fd:
    version_string = fd.read().strip()
    __version__ = version_string

# dynamic load long_description from long_description.rst
long_description_file = os.path.join(current_dir, 'long_description.rst')
with open(long_description_file, encoding="utf-8") as fd:
    ong_description_string = fd.read()
    __long_description__ = ong_description_string

default_model_dir = os.path.join(current_dir, 'model_data')
current_model_dir = default_model_dir

# global cache for dict_data
default_tokenizer = None


def get_dict_file(model_dir):
    return os.path.join(model_dir, 'dict.txt')


def _get_crf_file(model_dir):
    return os.path.join(model_dir, 'model.crfsuite')

# this is a jieba (https://github.com/fxsjy/jieba) compatible API
def _cut(message, HMM=False):
    initialize()

    if HMM:
        return default_tokenizer.cut_by_joint_model(message)
    else:
        return default_tokenizer.cut_by_DAG(message)


def _cut_by_DAG(message):
    initialize()

    return default_tokenizer.cut_by_DAG(message)


def _cut_by_HMM(message):
    initialize()

    return default_tokenizer.cut_by_HMM(message)


def _cut_by_CRF(message):
    initialize()

    return default_tokenizer.cut_by_CRF(message)


def _cut_by_joint_model(message):
    initialize()

    return default_tokenizer.cut_by_joint_model(message)


def _initialize():
    # put this code under the `default_mode_dir` to prevent import order issue
    # in case Tokenizer can't use `default_mode_dir` for it not be executed yet
    from MicroTokenizer.tokenizer import Tokenizer

    global default_tokenizer

    if default_tokenizer is None:
        default_tokenizer = Tokenizer()


def _load_model(model_path):
    global current_model_dir
    current_model_dir = model_path


def _load_default_model():
    global current_model_dir
    current_model_dir = default_model_dir

# below interfaces/functions are designed exactly equal to jieba's #


def _load_userdict(f):
    initialize()

    return default_tokenizer.load_user_dict(f)


def _load(name=None, **overrides):
    from . import util
    from . import about

    if name is None:
        name = about.__default_corpus__

    depr_path = overrides.get('path')
    if depr_path not in (True, False, None):
        deprecation_warning(Warnings.W001.format(path=depr_path))
    return util.load_model(name, **overrides)


from MicroTokenizer.tokenizers.max_match.backward import MaxMatchBackwardTokenizer as MaxMatchBackwardTokenizerV2
from MicroTokenizer.tokenizers.max_match.forward import MaxMatchForwardTokenizer as MaxMatchForwardTokenizerV2
from MicroTokenizer.tokenizers.max_match.bidirectional import MaxMatchBidirectionalTokenizer as MaxMatchBidirectionalTokenizerV2
from MicroTokenizer.tokenizers.dag_tokenizer import DAGTokenizer as DAGTokenizerV2
from MicroTokenizer.tokenizers.hmm_tokenizer import HMMTokenizer as HMMTokenizerV2
from MicroTokenizer.tokenizers.crf.tokenizer import CRFTokenizer as CRFTokenizerV2
from MicroTokenizer.ensemble.merge_solutions import MergeSolutions

max_match_backward_tokenizer_v2 = MaxMatchBackwardTokenizerV2.load(default_model_dir)
max_match_forward_tokenizer_v2 = MaxMatchForwardTokenizerV2.load(default_model_dir)
max_match_bidirectional_tokenizer_v2 = MaxMatchBidirectionalTokenizerV2.load(default_model_dir)
dag_tokenizer_v2 = DAGTokenizerV2.load(default_model_dir)
hmm_tokenizer_v2 = HMMTokenizerV2.load(default_model_dir)
crf_tokenizer_v2 = CRFTokenizerV2.load(default_model_dir)


def _cut_by_dag_hmm_joint_model(message):
    solutions = [
        dag_tokenizer_v2.segment(message),
        hmm_tokenizer_v2.segment(message)
    ]
    merge_solutions = MergeSolutions()
    best_solution = merge_solutions.merge(solutions)

    return best_solution

# this is a jieba (https://github.com/fxsjy/jieba) compatible API
def cut_v2(message, HMM=False):
    if HMM:
        return _cut_by_dag_hmm_joint_model(message)
    else:
        return dag_tokenizer_v2.segment(message)


# this is a jieba (https://github.com/fxsjy/jieba) compatible API
def load_userdict_v2(dict_file):
    return dag_tokenizer_v2.trie_tree.load_user_dict(dict_file)
