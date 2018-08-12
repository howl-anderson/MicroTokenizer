# -*- coding: utf-8 -*-

"""Top-level package for Micro Tokenizer for Chinese."""
import os

__author__ = """Xiaoquan Kong"""
__email__ = 'u1mail2me@gmail.com'
__version__ = '0.1.4'

current_dir = os.path.dirname(os.path.abspath(__file__))

_default_model_dir = os.path.join(current_dir, 'model_data')

default_model_dir = _default_model_dir

default_dag_dict_file = os.path.join(default_model_dir, 'dict.txt')
default_hmm_model_dir = default_model_dir

# global cache for dict_data
dict_data = None


def cut(message, HMM=False):
    if HMM:
        return cut_by_joint_model(message)
    else:
        return cut_by_DAG(message)


def cut_by_DAG(message):
    # NOTE: this import statement can not put the head line for it will cause cycle import
    from MicroTokenizer.dag import DAGTokenizer
    from MicroTokenizer.DAG.dictionary.trie_algorithm import TrieAlgorithm

    global dict_data

    if dict_data is None:
        raw_dict_data = TrieAlgorithm.read_dict(default_dag_dict_file)
        dict_data = TrieAlgorithm(
            TrieAlgorithm.process_data(raw_dict_data)
        )

    micro_tokenizer = DAGTokenizer(dict_data)
    micro_tokenizer.build_graph(message)
    micro_tokenizer.compute_shortest_path()

    graph_token = micro_tokenizer.get_tokens()
    message_token = graph_token[1:-1]  # remove start & end node which is not part of message
    return message_token


def cut_by_HMM(message):
    # NOTE: this import statement can not put the head line for it will cause cycle import
    from MicroTokenizer.hmm import HMMTokenizer

    hmm_tokenizer = HMMTokenizer.load_model(default_hmm_model_dir)

    message_token = hmm_tokenizer.predict(message)
    return message_token


def cut_by_joint_model(message):
    # NOTE: this import statement can not put the head line for it will cause cycle import
    from MicroTokenizer.merge_token import MergeSolutions
    solutions = [
        cut_by_DAG(message),
        cut_by_HMM(message)
    ]
    merge_solutions = MergeSolutions()
    best_solution = merge_solutions.merge(solutions)

    return best_solution


def load_model(model_path):
    global default_model_dir
    default_model_dir = model_path


def load_default_model():
    global default_model_dir
    default_model_dir = _default_model_dir
