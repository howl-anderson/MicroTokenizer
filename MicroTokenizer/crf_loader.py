import os
import cloudpickle

import pycrfsuite

from MicroTokenizer.base_loader import BaseLoader


class CRFLoader(BaseLoader):
    name = 'crf_based'

    def __init__(self, *args, **kwargs):
        super(CRFLoader, self).__init__(*args, **kwargs)

        self.crf_tagger = None
        self.model_file = None
        self.char2feature_func = None

    @staticmethod
    def get_model_file(model_dir):
        return os.path.join(str(model_dir), 'model.crfsuite')

    @staticmethod
    def get_char2feature_file(model_dir):
        return os.path.join(str(model_dir), 'char2feature.pickle')

    def from_disk(self, model_path, tokenizer_list, *args, **kwargs):
        self.model_file = self.get_model_file(model_path)

        self.crf_tagger = pycrfsuite.Tagger()
        self.crf_tagger.open(self.model_file)

        pickle_file = self.get_char2feature_file(model_path)
        with open(pickle_file, 'rb') as fd:
            self.char2feature_func = cloudpickle.load(fd)

        for tokenizer in tokenizer_list:
            tokenizer.assign_from_loader(
                crf_tagger=self.crf_tagger,
                word2features_func=self.char2feature_func
            )
