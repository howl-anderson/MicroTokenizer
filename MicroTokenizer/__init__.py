# -*- coding: utf-8 -*-

"""Top-level package for Micro Tokenizer for Chinese."""
import math
import os

__author__ = """Xiaoquan Kong"""
__email__ = 'u1mail2me@gmail.com'
__version__ = '0.1.0'

current_dir = os.path.dirname(os.path.abspath(__file__))

default_dict_file = os.path.join(current_dir, 'dictionary', 'dict.txt')

# global cache for dict_data
dict_data = None


def cut(message, HMM=False):
    if not HMM:
        return cut_by_DAG(message)
    else:
        return cut_by_HMM(message)


def cut_by_DAG(message):
    # NOTE: this import statement can not put the head line for it will cause cycle import
    from MicroTokenizer.MicroTokenizer import MicroTokenizer

    global dict_data

    if dict_data is None:
        dict_data = MicroTokenizer.read_dict(default_dict_file)
        MicroTokenizer.compute_edge_weight(dict_data)

    micro_tokenizer = MicroTokenizer(dict_data)
    micro_tokenizer.build_graph(message)

    graph_token = micro_tokenizer.get_tokens()
    message_token = graph_token[1:-1]  # remove start & end node which is not part of message
    return message_token


def cut_by_HMM(message):
    # NOTE: this import statement can not put the head line for it will cause cycle import
    from MicroTokenizer.hmm import HMMTokenizer

    default_model_dir = os.path.join(current_dir, 'hmm_model_data')
    hmm_tokenizer = HMMTokenizer.load_model(default_model_dir)

    message_token = hmm_tokenizer.predict(message)
    return message_token
