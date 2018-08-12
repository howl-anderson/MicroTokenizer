import math

from MicroTokenizer import default_dag_dict_file as default_dict_file


class DictionaryData(object):
    def __init__(self, dict_data=None):
        self.dict_data = None

        if dict_data is None:
            raw_dict_data = self.read_dict(default_dict_file)
            self.dict_data = self.process_data(raw_dict_data)
        else:
            self.dict_data = dict_data

    @staticmethod
    def read_dict(dict_file):
        dict_data = {}

        with open(dict_file, encoding='utf_8') as fd:
            for line in fd:
                splited_line = line.split(' ')
                data = dict(enumerate(splited_line))

                token = data[0]
                frequency = data[1].strip()  # using strip to clean tailing newline symbol
                part_of_speech = data.get(2, '').strip()  # using strip to clean tailing newline symbol

                # print(token, frequency)

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

    def write_to_file(self, output_file):
        # TODO: maybe will implement in future
        pass
