from typing import List


class BaseTokenizer(object):
    """Base class for all tokenizer"""

    @classmethod
    def load(cls, model_dir: str) -> "BaseTokenizer":
        """Load this tokenizer from model_dir"""
        raise NotImplementedError()

    def segment(self, message: str) -> List[str]:
        """Tokenize message and return the result"""
        raise NotImplementedError()

    def train(self, corpus: List[List[str]]) -> None:
        """
        Train this tokenizer by use corpus
        """
        raise NotImplementedError()

    def save(self, output_dir: str) -> None:
        """
        Dump model to directory
        A reverse process against with load_model()
        """
        raise NotImplementedError()
