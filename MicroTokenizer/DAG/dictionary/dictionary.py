import math


class DictionaryData(object):
    def __init__(self, dict_file=None, raw_dict_data=None):
        # TODO: check arguments is valid
        if raw_dict_data is None and dict_file is not None:
            raw_dict_data = self.read_dict(dict_file)

        self.dict_data = self.process_data(raw_dict_data)

    @staticmethod
    def read_dict(dict_file):
        dict_data = {}

        with open(dict_file) as fd:
            for line in fd:
                token, frequency = line.split()
                dict_data[token] = int(frequency)

        return dict_data

    @staticmethod
    def process_data(raw_dict_data):
        total_count = sum(raw_dict_data.values())

        return {k: math.log(total_count/v) for k, v in raw_dict_data.items()}

    def get_token_and_weight_at_text_head(self, text):
        raise NotImplemented

    def add_token_and_weight(self, token, weight):
        raise NotImplemented

    def load_user_dict(self, dict_file):
        with open(dict_file) as fd:
            for raw_line in fd:
                line = raw_line.strip()
                word, frequency_str = line.split()

                frequency_int = int(frequency_str)

                self.add_token_and_weight(word, frequency_int)

    def write_to_file(self, output_file):
        # TODO: maybe will implement in future
        pass
