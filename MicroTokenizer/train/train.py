from .train_hmm import train_hmm
from .train_dag import train_dag
from .train_crf import train_crf


def train(input_files_list, output_dir):
    train_dag(input_files_list, output_dir)
    train_hmm(input_files_list, output_dir)
    train_crf(input_files_list, output_dir)
