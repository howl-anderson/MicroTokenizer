#!/usr/bin/env python3
import os
from collections import Counter
from itertools import chain


def train_dag(input_files_list, output_dir):
    total_counter = Counter()
    for input_file in input_files_list:
        with open(input_file) as fd:
            counter = Counter(chain.from_iterable(map(str.split, fd)))
            total_counter += counter

    output_file = os.path.join(output_dir, 'dict.txt')

    with open(output_file, 'w') as fd:
        file_content_list = list(map(
            lambda x: "{} {}".format(x[0], x[1]),
            total_counter.most_common()
        ))

        file_content_str = "\n".join(file_content_list)
        fd.writelines(file_content_str)


if __name__ == "__main__":
    train_dag(["./data.txt"], "./dict.txt")
