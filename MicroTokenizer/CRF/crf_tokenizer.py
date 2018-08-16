import pycrfsuite

from MicroTokenizer.CRF.crf_trainer import CRFTrainer
from MicroTokenizer.seq2seq.BMES import decoding


class CRFTokenizer:
    def __init__(self, model_file):
        self.crf_tagger = pycrfsuite.Tagger()
        self.crf_tagger.open(model_file)

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

    def cut(self, char_list):
        char_tag_list = self.predict_char_tag(char_list)

        return decoding(char_tag_list)


if __name__ == "__main__":
    crf_tokenizer = CRFTokenizer("/Users/howl/Repositories/MicroTokenizer/MicroTokenizer/model_data/model.crfsuite")
    result = crf_tokenizer.cut("24口交换机")

    print(result)
