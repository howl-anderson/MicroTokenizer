# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from typing import List
from collections import Counter

import six


class TrainDictionary:
    def __init__(self):
        self.dictionary = {}
        self.counter = Counter()

    def train_one_line(self, token_list):
        # type: (List[str]) -> None

        counter = Counter(token_list)
        self.counter += counter

    def do_train(self):
        self.dictionary = dict(self.counter.most_common())

    def persist_to_dir(self, output_dir):
        # type: (str) -> None

        dictionary_file = os.path.join(output_dir, 'dict.txt')

        file_content = '\n'.join(
            ["{}\t{}".format(k, v) for k, v in self.dictionary.items()]
        )

        with open(dictionary_file, 'wt') as fd:
            if six.PY2:
                file_content = file_content.encode('utf-8')

            fd.write(file_content)
            fd.write('\n')  # write tail newline
