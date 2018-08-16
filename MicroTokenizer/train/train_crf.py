#!/usr/bin/env python
import os

from MicroTokenizer.CRF.crf_trainer import CRFTrainer
from tqdm import tqdm


def train_hmm(input_files_list, output_dir):
    crf_trainer = CRFTrainer()

    for data_file in input_files_list:
        with open(data_file) as fd:
            for line in tqdm(fd):
                crf_trainer.train_one_raw_line(line)

    crf_trainer.train(output_dir)


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    train_hmm(
        [os.path.join(current_dir, "./data.txt")],
        os.path.join(current_dir, "./model.crfsuite")
    )
