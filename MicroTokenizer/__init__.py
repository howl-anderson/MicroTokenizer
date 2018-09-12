# coding: utf8
from __future__ import unicode_literals

from .about import __version__
from .errors import Warnings, deprecation_warning

"""Top-level package for Micro Tokenizer for Chinese."""
import os

__author__ = """Xiaoquan Kong"""
__email__ = 'u1mail2me@gmail.com'
__version__ = ''
__long_description__ = ''

current_dir = os.path.dirname(os.path.abspath(__file__))

# dynamic load version from version file
version_file = os.path.join(current_dir, 'version.txt')
with open(version_file) as fd:
    version_string = fd.read().strip()
    __version__ = version_string

# dynamic load long_description from long_description.rst
long_description_file = os.path.join(current_dir, 'long_description.rst')
with open(long_description_file) as fd:
    ong_description_string = fd.read()
    __long_description__ = ong_description_string

default_model_dir = os.path.join(current_dir, 'model_data')
current_model_dir = default_model_dir

# global cache for dict_data
default_tokenizer = None


def get_dict_file(model_dir):
    return os.path.join(model_dir, 'dict.txt')


def get_crf_file(model_dir):
    return os.path.join(model_dir, 'model.crfsuite')


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


def cut_by_CRF(message):
    initialize()

    return default_tokenizer.cut_by_CRF(message)


def cut_by_joint_model(message):
    initialize()

    return default_tokenizer.cut_by_joint_model(message)


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

# below interfaces/functions are designed exactly equal to jieba's #


def load_userdict(f):
    initialize()

    return default_tokenizer.load_user_dict(f)


def load(name=None, **overrides):
    from . import util
    from . import about

    if name is None:
        name = about.__default_corpus__

    depr_path = overrides.get('path')
    if depr_path not in (True, False, None):
        deprecation_warning(Warnings.W001.format(path=depr_path))
    return util.load_model(name, **overrides)
