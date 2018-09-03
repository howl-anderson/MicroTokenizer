import os
from typing import List
from warnings import warn

import pycrfsuite

from MicroTokenizer.CRF.crf_trainer import CRFTrainer
from MicroTokenizer.base_tokenizer import BaseTokenizer
from MicroTokenizer.seq2seq.BMES import decoding


class CRFTokenizer(BaseTokenizer):
    def __init__(self, *args, **kwargs):
        super(CRFTokenizer, self).__init__(*args, **kwargs)

        self.model_file = self.get_model_file(self.model_dir)
        self.crf_tagger = None

        self.crf_trainer = CRFTrainer()

        self.open_mode = None
        self.file_content = None

    @staticmethod
    def get_model_file(model_dir):
        return os.path.join(model_dir, 'model.crfsuite')

    def load_model(self):
        self.crf_tagger = pycrfsuite.Tagger()
        self.crf_tagger.open(self.model_file)

    def predict_char_tag(self, char_list):
        tag_list = self.predict_tag(char_list)

        return list(zip(char_list, tag_list))

    def predict_tag(self, char_list):
        feature_list = [
            CRFTrainer._default_word2features(char_list, i)
            for i in range(len(char_list))
        ]

        tag_list = self.crf_tagger.tag(feature_list)

        return tag_list

    def segment(self, message):
        # type: (str) -> List[str]

        char_tag_list = self.predict_char_tag(message)

        return decoding(char_tag_list)

    def train_one_line(self, token_list):
        # type: (List[str]) -> None

        self.crf_trainer.train_one_line_by_token(token_list)

    def do_train(self):
        warn(
            "During to the limit of pycrfsuite: do_train will do nothing, "
            "persist_to_dir will do real train work."
            "Also because no training here, model for this instance will not update"
        )

    def persist_to_dir(self, output_dir):
        # type: (str) -> None

        # TODO: should persist feature function as well
        model_file = self.get_model_file(output_dir)

        self.crf_trainer.train(model_file)
