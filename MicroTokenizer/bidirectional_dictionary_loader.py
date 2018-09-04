from MicroTokenizer.DAG.dictionary.trie_algorithm import TrieAlgorithm
from MicroTokenizer.backward_dictionary_loader import \
    BackwardDictionaryBasedLoader
from MicroTokenizer.base_dictionary_based_loader import BaseDictionaryBasedLoader
from MicroTokenizer.forward_dictionary_loader import \
    ForwardDictionaryBasedLoader
from MicroTokenizer.max_match.backward import MaxMatchBackwardTokenizer
from MicroTokenizer.max_match.forward import MaxMatchForwardTokenizer


class BidirectionalDictionaryBasedLoader(BaseDictionaryBasedLoader):
    name = 'bidirectional_dictionary_based'

    def __init__(self, *args, **kwargs):
        super(BidirectionalDictionaryBasedLoader, self).__init__(*args, **kwargs)

    def from_disk(self, model_path, tokenizer_list, *args, **kwargs):
        # type: (str, List[BaseTokenizer]) -> None

        backward_tokenizer = MaxMatchBackwardTokenizer()
        forward_tokenizer = MaxMatchForwardTokenizer()

        backward_loader = BackwardDictionaryBasedLoader.instance()
        forward_loader = ForwardDictionaryBasedLoader.instance()

        backward_loader.from_disk(None, [backward_tokenizer])
        forward_loader.from_disk(None, [forward_tokenizer])

        for tokenizer in tokenizer_list:
            tokenizer.assign_from_loader(backward_tokenizer=backward_tokenizer, forward_tokenizer=forward_tokenizer)

    skip_load_from_disk = True
