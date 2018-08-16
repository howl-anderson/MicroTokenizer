def decoding(char_tag_pair):
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
