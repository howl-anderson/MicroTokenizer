import warnings

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


def get_trainer_list(enable_list=None, disable_list=None):
    if enable_list and disable_list:
        warnings.warn(
            "User can not use both enable_list and disable_list at same time."
            "For now, disable_list will take the priority."
        )

        enable_list = None

    # default trainer_list is all trainer
    trainer_list = set(trainer_registry.values())

    if enable_list:
        trainer_list = {v for k, v in trainer_registry.items()
                        if k in enable_list}

    if disable_list:
        trainer_list = {v for k, v in trainer_registry.items()
                        if k not in trainer_list}

    return trainer_list
