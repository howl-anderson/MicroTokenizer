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
        raise NotImplemented

    def segment(self, message):
        # type: (str) -> List[str]
        raise NotImplemented

    def train_one_line(self, token_list):
        # type: ( List[str]) -> None
        raise NotImplemented

    def do_train(self):
        raise NotImplemented

    def persist_to_dir(self, output_dir):
        # type: (str) -> None
        raise NotImplemented

    def get_loader(self):
        raise NotImplemented

    def assign_from_loader(self, *args, **kwargs):
        raise NotImplemented
