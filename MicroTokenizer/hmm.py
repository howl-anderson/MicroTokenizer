from typing import List

from MicroHMM.hmm import HMMModel

from MicroTokenizer.hmm_loader import HMMLoader
from MicroTokenizer.base_tokenizer import BaseTokenizer


class HMMTokenizer(BaseTokenizer):
    def __init__(self, *args, **kwargs):
        super(HMMTokenizer, self).__init__(*args, **kwargs)

        self.hmm_model = HMMModel()  # type: HMMModel

    def train_one_line(self, token_list):
        list_of_word_tag_pair = []
        for word in token_list:
            word = word.strip()

            tag = self._generate_char_tag_for_word(word)

            list_of_word_tag_pair.extend(
                list(zip(word, tag))
            )

        self.hmm_model.train_one_line(list_of_word_tag_pair)

    def do_train(self):
        self.hmm_model.do_train()

    @staticmethod
    def _generate_char_tag_for_word(word):
        # TODO: tag set related function should go to a standalone package
        len_of_word = len(word)

        if len_of_word == 1:
            return 'S'

        if len_of_word >= 2:
            number_of_middle = len_of_word - 2
            return 'B' + 'M' * number_of_middle + 'E'

    def predict(self, line, output_graphml_file=None):
        char_list = line

        char_tag_pair = self.hmm_model.predict(char_list, output_graphml_file)

        # TODO: current BMES decoding is not good, can't raise decoding exception

        token_list = []
        word_char = []
        for char, tag in char_tag_pair:
            # no matter what, word_char still need record
            word_char.append(char)

            if tag == "S" or tag == "E":
                # emission token word
                word = "".join(word_char)
                token_list.append(word)

                # reset word_char cache
                word_char = []

        # no matter what, char can not disappear
        if word_char:
            word = "".join(word_char)
            token_list.append(word)

        return token_list

    def segment(self, message):
        # type: (str) -> List[str]

        return self.predict(message)

    def load_model(self):
        self.hmm_model = HMMModel.load_model(self.model_dir)

    def persist_to_dir(self, output_dir):
        # type: (str) -> None
        self.hmm_model.save_model(output_dir)

    def assign_from_loader(self, *args, **kwargs):
        self.hmm_model = kwargs['hmm_model']

    def get_loader(self):
        return HMMLoader
