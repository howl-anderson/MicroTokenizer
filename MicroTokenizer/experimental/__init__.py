from MicroTokenizer import (
    max_match_backward_tokenizer,
    max_match_bidirectional_tokenizer,
    max_match_forward_tokenizer,
    dag_tokenizer,
    hmm_tokenizer,
    crf_tokenizer,
)
from MicroTokenizer.ensemble.merge_solutions import MergeSolutions
from MicroTokenizer.pipeline import PipelineUnicodeScriptTokenizer
from MicroTokenizer.tokenizers.whitespace_split_tokenizer import (
    WhitespaceSplitTokenizer,
)

whitespace_split_tokenizer = WhitespaceSplitTokenizer()

max_match_backward_tokenizer = PipelineUnicodeScriptTokenizer(
    {"Han": max_match_backward_tokenizer, "Common": whitespace_split_tokenizer}
)
max_match_forward_tokenizer = PipelineUnicodeScriptTokenizer(
    {"Han": max_match_forward_tokenizer, "Common": whitespace_split_tokenizer}
)
max_match_bidirectional_tokenizer = PipelineUnicodeScriptTokenizer(
    {"Han": max_match_bidirectional_tokenizer, "Common": whitespace_split_tokenizer}
)
dag_tokenizer = PipelineUnicodeScriptTokenizer(
    {"Han": dag_tokenizer, "Common": whitespace_split_tokenizer}
)
hmm_tokenizer = PipelineUnicodeScriptTokenizer(
    {"Han": hmm_tokenizer, "Common": whitespace_split_tokenizer}
)
crf_tokenizer = PipelineUnicodeScriptTokenizer(
    {"Han": crf_tokenizer, "Common": whitespace_split_tokenizer}
)


def _cut_by_dag_hmm_joint_model(message):
    solutions = [dag_tokenizer.segment(message), hmm_tokenizer.segment(message)]
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
