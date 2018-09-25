# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import copy
from functools import reduce

import pycrfsuite
import six
from tokenizer_tools.tagset.BMES import BMESEncoderDecoder

tag_encoder_decoder = BMESEncoderDecoder()


class CRFTrainer:
    _default_params = {
        'c1': 0.1,  # coefficient for L1 penalty
        'c2': 0.01,  # coefficient for L2 penalty
        'max_iterations': 200,  # stop earlier

        # include transitions that are possible, but not observed
        'feature.possible_transitions': True
    }

    def __init__(self, feature_func_list=None):
        self.crf_trainer = pycrfsuite.Trainer(verbose=False)

        self.feature_func_list = feature_func_list

        if not self.feature_func_list:
            self.feature_func_list = default_feature_func_list

    def train_one_raw_line(self, blank_splittable_string):
        token_list = blank_splittable_string.split()

        self.train_one_line_by_token(token_list)

    def train_one_line_by_char_tag(self, char_list, tag_list):
        feature_list = get_feature_list(char_list, self.feature_func_list)

        self.train_one_line(feature_list, tag_list)

    def train_one_line_by_token(self, token_list):
        # drop blank line
        if not token_list:
            return None

        tag_list = reduce(
            lambda x, y: x + y,
            [
                # default coding schema is BMES
                tag_encoder_decoder.encode_word(i)
                for i in token_list
            ],
        )
        char_list = reduce(
            lambda x, y: x + y,
            token_list
        )

        self.train_one_line_by_char_tag(char_list, tag_list)

    def train_one_line(self, x, y):
        self.crf_trainer.append(x, y)

    def set_params(self, **kwargs):
        params = copy.deepcopy(self._default_params)

        params.update(kwargs)

        self.crf_trainer.set_params(params)

    def train(self, output_file):
        self.crf_trainer.train(output_file)


feature_func_dict = {
    'bias': lambda sent, i: None,
    'char': lambda sent, i: sent[i],
    '-1:char': lambda sent, i: sent.get(i - 1, ''),
    '-1/0:char': lambda sent, i: sent.get(i - 1, '') + '/' + sent[i],
    '-2:char': lambda sent, i: sent.get(i - 2, ''),
    '-2/-1:char': lambda sent, i: sent.get(i - 2, '') + '/' + sent.get(i - 1, ''),
    '-2/-1/0:char': lambda sent, i: sent.get(i - 2, '') + '/' + sent.get(i - 1, '') + '/' + sent[i],
    '+1:char': lambda sent, i: sent.get(i + 1, ''),
    '0/+1:char': lambda sent, i: sent[i] + '/' + sent.get(i + 1, ''),
    '+2:char': lambda sent, i: sent.get(i + 2, ''),
    '+1/+2:char': lambda sent, i: sent.get(i + 1, '') + '/' + sent.get(i + 2, ''),
    '0/+1/+2:char': lambda sent, i: sent[i] + '/' + sent.get(i + 1, '') + '/' + sent.get(i + 2, ''),
    '-1/0/+1:char': lambda sent, i: sent.get(i - 1, '') + '/' + sent[i] + '/' + sent.get(i + 1, ''),
    '-1/+1:char': lambda sent, i: sent.get(i - 1, '') + '/' + sent.get(i + 1, ''),
}


class DictLikeSequence(six.text_type):
    def get(self, index, default=None):
        try:
            return self[index]
        except IndexError:
            return default


def word2features(sent, i, feature_func_list):
    # if six.PY2:
    #     sent = sent.encode('utf-8')

    # make sure is a DictLikeSequence which can using get(index, default_value)
    sent = DictLikeSequence(sent)

    feature_list = []
    for feature_func_name in feature_func_list:
        feature_func = feature_func_dict.get(feature_func_name)
        feature_value = feature_func(sent, i)

        if feature_value is None:
            # special for bias
            feature = feature_func_name
        else:
            feature = feature_func_name + '=' + feature_value

        feature_list.append(feature)

    return feature_list


def get_feature_list(sent, feature_func_list):
    feature_list = [
        word2features(sent, i, feature_func_list)
        for i in range(len(sent))
    ]

    return feature_list


all_feature_func_list = list(feature_func_dict.keys())

regular_feature_func_list = [
    'bias',
    'char',
    '-1:char',
    '-1/0:char',
    '+1:char',
    '0/+1:char',
]

default_feature_func_list = regular_feature_func_list
