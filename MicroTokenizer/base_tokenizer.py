from typing import (
    List
)

from MicroTokenizer import default_model_dir


class BaseTokenizer(object):
    """Base class for all tokenizer"""

    def __init__(self, model_dir=None, *args, **kwargs):
        if model_dir is None:
            model_dir = default_model_dir

        self.model_dir = model_dir

    def load_model(self):
        """load model from default location (inside the package data dir)"""
        raise NotImplementedError()

    def segment(self, message: str) -> List[str]:
        """Tokenize message and return the result"""
        raise NotImplementedError()

    def train_one_line(self, token_list: List[str]) -> None:
        """
        Train this tokenizer by one sample.
        Notice: this is not real train. do_train() will do the real job.
                remember to call do_train()
        """
        raise NotImplementedError()

    def do_train(self):
        """
        Do the real train work.
        This is required for train_one_line()
        """
        # TODO(Xiaoquan Kong): provide a context manager for training may have a better user experience
        raise NotImplementedError()

    def persist_to_dir(self, output_dir: str) -> None:
        """
        Dump model to directory
        A reverse process against with load_model()
        """
        raise NotImplementedError()

    def get_loader(self):
        raise NotImplementedError()

    def assign_from_loader(self, *args, **kwargs):
        raise NotImplementedError()
