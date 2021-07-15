import warnings

from MicroTokenizer.tokenizers.hmm_tokenizer import HMMTokenizer
from MicroTokenizer.tokenizers.dag_tokenizer import DAGTokenizer
from MicroTokenizer.tokenizers.crf.tokenizer import CRFTokenizer
from MicroTokenizer.tokenizers.max_match.bidirectional import (
    MaxMatchBidirectionalTokenizer,
)
from MicroTokenizer.tokenizers.max_match.forward import MaxMatchForwardTokenizer
from MicroTokenizer.tokenizers.max_match.backward import MaxMatchBackwardTokenizer

trainer_registry = {
    HMMTokenizer: HMMTokenizer,
    DAGTokenizer: DAGTokenizer,
    CRFTokenizer: CRFTokenizer,
    MaxMatchForwardTokenizer: MaxMatchForwardTokenizer,
    MaxMatchBackwardTokenizer: MaxMatchBackwardTokenizer,
    MaxMatchBidirectionalTokenizer: MaxMatchBidirectionalTokenizer,
}


def get_trainer_list(enable_list=None, disable_list=None, *args, **kwargs):
    if enable_list and disable_list:
        warnings.warn(
            "User can not use both enable_list and disable_list at same time."
            "For now, disable_list will take the priority."
        )

        enable_list = None

    # default trainer_list is all trainer
    trainer_list = set(trainer_registry.values())

    if enable_list:
        trainer_list = {v for k, v in trainer_registry.items() if k in enable_list}

    if disable_list:
        trainer_list = {v for k, v in trainer_registry.items() if k not in trainer_list}

    return trainer_list
