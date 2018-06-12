# -*- coding: utf-8 -*-

"""Top-level package for Micro Tokenizer for Chinese."""
import math
import os

__author__ = """Xiaoquan Kong"""
__email__ = 'u1mail2me@gmail.com'
__version__ = '0.1.0'

current_dir = os.path.dirname(os.path.abspath(__file__))

default_dict_file = os.path.join(current_dir, 'dictionary', 'dict.txt')


def read_dict(dict_file):
    dict_data = {}

    with open(dict_file) as fd:
        for line in fd:
            splited_line = line.split(' ')
            data = dict(enumerate(splited_line))

            token = data[0]
            frequency = data[1].strip()  # using strip to clean tailing newline symbol
            part_of_speech = data.get(2, '').strip()  # using strip to clean tailing newline symbol

            # print(token, frequency)

            dict_data[token] = int(frequency)

    return dict_data


def compute_edge_weight(dict_data):
    # get total weight count for compute possibility
    total_weight = sum(dict_data.values())

    # recompute the weight
    for k, v in dict_data.items():
        # possibility = count / total_count
        # reciprocal of possibility can turn max value to min value, which can be
        # used for search max value path by search shortest path
        # log function can turn multiplication to addition: log(A * B) = log(A) + log(B)
        dict_data[k] = math.log(total_weight / v)


dict_data = read_dict(default_dict_file)
compute_edge_weight(dict_data)


def cut(message):
    from MicroTokenizer.MicroTokenizer import MicroTokenizer

    micro_tokenizer = MicroTokenizer(dict_data)
    micro_tokenizer.build_graph(message)

    graph_token = micro_tokenizer.get_tokens()
    message_token = graph_token[1:-1]  # remove start & end node which is not part of message
    return message_token
