#!/usr/bin/env python

from MicroTokenizer.hmm import HMMTokenizer
from tqdm import tqdm


def train_hmm(input_files_list, output_dir):
    hmm_tokenizer = HMMTokenizer()

    for data_file in input_files_list:
        with open(data_file) as fd:
            for line in tqdm(fd):
                hmm_tokenizer.train_one_line(line)

    hmm_tokenizer.hmm_model.do_train()
    hmm_tokenizer.hmm_model.save_model(output_dir)


if __name__ == "__main__":
    train_hmm(["./data.txt"], "./dict.txt")
