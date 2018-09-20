import copy
from functools import reduce

import pycrfsuite
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

    def __init__(self, char2feature_func=None):
        self.crf_trainer = pycrfsuite.Trainer(verbose=False)

        if not char2feature_func:
            self.char2feature_func = default_word2features

    def train_one_raw_line(self, blank_splittable_string):
        token_list = blank_splittable_string.split()

        self.train_one_line_by_token(token_list)

    def train_one_line_by_char_tag(self, char_list, tag_list):
        feature_list = [
            self.char2feature_func(char_list, i) for i in range(len(char_list))
        ]

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


def default_word2features(sent, i):
    char = sent[i]
    sent_len = len(sent)

    features = [
        'bias',
        'char=' + char
    ]
    if i > 0:
        prev_one_word = sent[i - 1]
        features.extend([
            '-1:char=' + prev_one_word,
            '-1/0:char=' + prev_one_word + '/' + char
        ])
    else:
        features.append('BOS')

    if i > 1:
        prev_two_word = sent[i - 2]
        prev_one_word = sent[i - 1]

        features.extend([
            '-2:char=' + prev_two_word,
            '-2/-1:char=' + '/'.join([prev_two_word, prev_one_word]),
            '-2/-1/0:char=' + '/'.join([prev_two_word, prev_one_word, char])
        ])
    else:
        features.append('near_BOS')

    if i < sent_len - 1:
        next_one_word = sent[i + 1]
        features.extend([
            '+1:char' + next_one_word,
            '0/+1:char' + '/'.join([char, next_one_word])
        ])
    else:
        features.append('EOS')

    if i < sent_len - 2:
        next_two_word = sent[i + 2]
        next_one_word = sent[i + 1]

        features.extend([
            '+2:char' + next_two_word,
            '+1/+2:char=' + '/'.join([next_one_word, next_two_word]),
            '0/+1/+2:char=' + '/'.join([char, next_one_word, next_two_word])
        ])
    else:
        features.append('near_EOS')

    if 0 < i < sent_len - 1:
        prev_one_word = sent[i - 1]
        next_one_word = sent[i + 1]

        features.append('-1/0/+1:char=' + '/'.join([prev_one_word, char, next_one_word]))
        features.append('-1/+1:char=' + '/'.join([prev_one_word, next_one_word]))

    return features
