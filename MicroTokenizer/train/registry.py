from MicroTokenizer.hmm import HMMTokenizer
from MicroTokenizer.dag import DAGTokenizer
from MicroTokenizer.CRF.crf_tokenizer import CRFTokenizer
from MicroTokenizer.max_match.bidirectional import MaxMatchBidirectionalTokenizer
from MicroTokenizer.max_match.forward import MaxMatchForwardTokenizer
from MicroTokenizer.max_match.backward import MaxMatchBackwardTokenizer
from MicroTokenizer.base_dictionary_based_tokenizer import BaseDictionaryBasedTokenizer

trainer_registry = {
    HMMTokenizer: HMMTokenizer,
    DAGTokenizer: BaseDictionaryBasedTokenizer,
    CRFTokenizer: CRFTokenizer,
    MaxMatchForwardTokenizer: BaseDictionaryBasedTokenizer,
    MaxMatchBackwardTokenizer: BaseDictionaryBasedTokenizer,
    MaxMatchBidirectionalTokenizer: BaseDictionaryBasedTokenizer
}

trainer_list = set(trainer_registry.values())
