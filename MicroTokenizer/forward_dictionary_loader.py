from MicroTokenizer.base_dictionary_based_loader import BaseDictionaryBasedLoader


class ForwardDictionaryBasedLoader(BaseDictionaryBasedLoader):
    name = 'forward_dictionary_based'

    def __init__(self, *args, **kwargs):
        super(ForwardDictionaryBasedLoader, self).__init__(*args, **kwargs)

    def from_disk(self, model_path, tokenizer_list, *args, **kwargs):
        super(ForwardDictionaryBasedLoader, self).from_disk(model_path, tokenizer_list)
