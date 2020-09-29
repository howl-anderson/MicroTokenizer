from typing import (
    List
)

from MicroTokenizer import default_model_dir


class BaseTokenizer(object):
    def __init__(self, model_dir=None, *args, **kwargs):
        if model_dir is None:
            model_dir = default_model_dir

        self.model_dir = model_dir

    def load_model(self):
        raise NotImplementedError()

    def segment(self, message):
        # type: (str) -> List[str]
        raise NotImplementedError()

    def train_one_line(self, token_list):
        # type: ( List[str]) -> None
        raise NotImplementedError()

    def do_train(self):
        raise NotImplementedError()

    def persist_to_dir(self, output_dir):
        # type: (str) -> None
        raise NotImplementedError()

    def get_loader(self):
        raise NotImplementedError()

    def assign_from_loader(self, *args, **kwargs):
        raise NotImplementedError()
