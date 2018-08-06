from .train_hmm import train_hmm
from .train_dag import train_dag


def train(input_files_list, output_dir):
    train_dag(input_files_list, output_dir)
    train_hmm(input_files_list, output_dir)
