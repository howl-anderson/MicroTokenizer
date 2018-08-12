# -*- coding: utf-8 -*-

"""Top-level package for Micro Tokenizer for Chinese."""
import os

__author__ = """Xiaoquan Kong"""
__email__ = 'u1mail2me@gmail.com'
__version__ = '0.1.5'

current_dir = os.path.dirname(os.path.abspath(__file__))

default_model_dir = os.path.join(current_dir, 'model_data')
current_model_dir = default_model_dir

# global cache for dict_data
default_tokenizer = None


def get_dict_file(model_dir):
    return os.path.join(model_dir, 'dict.txt')


def cut(message, HMM=False):
    initialize()

    if HMM:
        return default_tokenizer.cut_by_joint_model(message)
    else:
        return default_tokenizer.cut_by_DAG(message)


def cut_by_DAG(message):
    initialize()

    return default_tokenizer.cut_by_DAG(message)


def cut_by_HMM(message):
    initialize()

    return default_tokenizer.cut_by_HMM(message)


def cut_by_joint_model(message):
    initialize()

    return default_tokenizer.cut_by_join_model(message)


def initialize():
    # put this code under the `default_mode_dir` to prevent import order issue
    # in case Tokenizer can't use `default_mode_dir` for it not be executed yet
    from MicroTokenizer.tokenizer import Tokenizer

    global default_tokenizer

    if default_tokenizer is None:
        default_tokenizer = Tokenizer()


def load_model(model_path):
    global current_model_dir
    current_model_dir = model_path


def load_default_model():
    global current_model_dir
    current_model_dir = default_model_dir
