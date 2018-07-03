from MicroHMM.hmm import HMMModel


class HMMTokenizer(object):
    def __init__(self, hmm_model=None):
        self.hmm_model = HMMModel() if hmm_model is None else hmm_model

    def train_one_line(self, line):
        line = line.strip()

        list_of_word_tag_pair = []
        for word in line.split():
            word = word.strip()

            tag = self._generate_char_tag_for_word(word)

            list_of_word_tag_pair.extend(
                list(zip(word, tag))
            )

        self.hmm_model.train_one_line(list_of_word_tag_pair)

    @staticmethod
    def _generate_char_tag_for_word(word):
        len_of_word = len(word)

        if len_of_word == 1:
            return 'S'

        if len_of_word >= 2:
            number_of_middle = len_of_word - 2
            return 'B' + 'M' * number_of_middle + 'E'

    def predict(self, line, output_graphml_file=None):
        char_list = line

        char_tag_pair = self.hmm_model.predict(char_list, output_graphml_file)

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

        return token_list

    @classmethod
    def load_model(cls, model_dir="model"):
        hmm_model = HMMModel.load_model(model_dir)

        return cls(hmm_model)


if __name__ == "__main__":
    hmm_tokenizer = HMMTokenizer()
    hmm_tokenizer.train_one_line("我/A 是/B 中国人/C")
    hmm_tokenizer.train_one_line("你/A 打/B 人/C")
    result = hmm_tokenizer.predict("你 打 人")
    print(result)
