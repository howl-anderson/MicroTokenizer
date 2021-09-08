from typing import List, Tuple


class BMESEncoderDecoder:
    """
    Encoder and Decoder for BMES tag scheme
    """

    def __init__(self, addition_m_tag_num=0):
        # TODO: using addition_m_tag_num to
        # generate BM1ES BM1M2S BM1M2MS tag scheme
        self.addition_m_tag_num = addition_m_tag_num

        self.possible_m_tag = [
            "M{}".format(i + 1) for i in range(self.addition_m_tag_num)
        ] + ["M"]

    def generate_m_tag_by_char_length(self, word_length):
        number_of_middle = word_length - 2
        if number_of_middle > self.addition_m_tag_num:
            addition_m = ["M{}".format(i + 1) for i in range(self.addition_m_tag_num)]
            padding_m = ["M"] * (number_of_middle - self.addition_m_tag_num)
        else:
            addition_m = ["M{}".format(i + 1) for i in range(number_of_middle)]
            padding_m = []

        return addition_m + padding_m

    def encode_word(self, word: str) -> str:
        """
        encode a word to BMES scheme as string

        :param word: string
        :return: string
        """

        tag_list = self.encode_word_by_tag_list(word)

        return "".join(tag_list)

    def encode_word_by_tag_list(self, word: str) -> List[str]:
        """
        encode a word to BEMS scheme as list of string

        :param word: string
        :return: List[str]
        """

        len_of_word = len(word)

        if len_of_word == 1:
            return ["S"]
        else:
            return ["B"] + self.generate_m_tag_by_char_length(len_of_word) + ["E"]

    def encode_word_list(self, word_list: List[str]) -> List[str]:
        return [self.encode_word(i) for i in word_list]

    def encode_word_list_as_string(self, word_list):
        # type: (List[str]) -> str

        return "".join(self.encode_word_list(word_list))

    def decode_tag(self, tag_list: List[str]) -> List[Tuple[int, int]]:
        def _decoding_exception(tag_list, i):
            return ValueError("Decoding error near end of {}".format(tag_list[: i + 1]))

        def _process_word(word_list_slice, previous_tags, i):
            word_list_slice.append((i - len(previous_tags) + 1, i + 1))
            previous_tags[:] = []

        word_list_slice = []
        possible_ending_tag = self.possible_m_tag + ["E"]

        previous_tags = []
        for i, tag in enumerate(tag_list):
            if not previous_tags:  # start a new token
                if tag not in ("B", "S"):
                    raise _decoding_exception(tag_list, i)

                previous_tags.append(tag)

                if tag == "S":
                    _process_word(word_list_slice, previous_tags, i)
            else:
                if tag not in possible_ending_tag:
                    raise _decoding_exception(tag_list, i)

                previous_tags.append(tag)

                if tag == "E":
                    _process_word(word_list_slice, previous_tags, i)

        return word_list_slice

    def decode_char_tag_pair(self, char_tag_pair: List[Tuple[str, str]]) -> List[str]:
        tag_list = [i[1] for i in char_tag_pair]

        word_list_slice = self.decode_tag(tag_list)

        word_tag_list = [char_tag_pair[i:j] for i, j in word_list_slice]
        word_list = ["".join([j[0] for j in i]) for i in word_tag_list]

        return word_list
