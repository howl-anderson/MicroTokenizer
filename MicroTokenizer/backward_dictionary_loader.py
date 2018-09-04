from MicroTokenizer.base_dictionary_based_loader import BaseDictionaryBasedLoader


class BackwardDictionaryBasedLoader(BaseDictionaryBasedLoader):
    name = 'backward_dictionary_based'

    def __init__(self, *args, **kwargs):
        super(BackwardDictionaryBasedLoader, self).__init__(*args, **kwargs)

    def from_disk(self, model_path, tokenizer_list, *args, **kwargs):
        super(BackwardDictionaryBasedLoader, self).from_disk(model_path, tokenizer_list, reverse=True)
