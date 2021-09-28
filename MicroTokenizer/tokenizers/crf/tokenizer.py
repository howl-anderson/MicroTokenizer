import os
import pickle
from typing import List
from warnings import warn

import pycrfsuite

from MicroTokenizer.tokenizers.crf.trainer import (
    CRFTrainer,
    default_feature_func_list,
    get_feature_list,
)
from MicroTokenizer.encoding.BMES import decoding
from MicroTokenizer.tokenizers.base_tokenizer import BaseTokenizer


class CRFTokenizer(BaseTokenizer):
    def __init__(self, crf_tagger=None, feature_func_list=None):
        # for inference
        self.crf_tagger = crf_tagger
        self.feature_func_list = (
            feature_func_list if feature_func_list else default_feature_func_list
        )
        # for training
        self.crf_trainer = CRFTrainer(self.feature_func_list)

    @staticmethod
    def get_model_file(model_dir):
        return os.path.join(model_dir, "model.crfsuite")

    @staticmethod
    def get_char2feature_file(model_dir):
        return os.path.join(model_dir, "feature_func_list.pickle")

    @classmethod
    def load(cls, model_dir: str):
        model_file = cls.get_model_file(model_dir)
        crf_tagger = pycrfsuite.Tagger()
        crf_tagger.open(model_file)

        pickle_file = cls.get_char2feature_file(model_dir)
        with open(pickle_file, "rb") as fd:
            feature_func_list = pickle.load(fd)

        return cls(crf_tagger, feature_func_list)

    def predict_char_tag(self, char_list):
        tag_list = self.predict_tag(char_list)

        return list(zip(char_list, tag_list))

    def predict_tag(self, char_list):
        feature_list = get_feature_list(char_list, self.feature_func_list)

        tag_list = self.crf_tagger.tag(feature_list)

        return tag_list

    def segment(self, message: str) -> List[str]:

        char_tag_list = self.predict_char_tag(message)

        return decoding(char_tag_list)

    def train(self, corpus):
        for token_list in corpus:
            self.crf_trainer.train_one_line_by_token(token_list)

        warn(
            "During to the limit of pycrfsuite: do_train will do nothing, "
            "persist_to_dir will do real train work."
            "Also because no training here, model for this instance will not update"
        )

    def save(self, output_dir: str):
        # TODO: should persist feature function as well
        model_file = self.get_model_file(output_dir)

        self.crf_trainer.train(model_file)

        pickle_file = self.get_char2feature_file(output_dir)
        with open(pickle_file, "wb") as fd:
            # using protocol=2 to keep compatible with python 2
            pickle.dump(self.feature_func_list, fd, protocol=2)
