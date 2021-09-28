import yaml

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
        trainer_list = {v for k, v in trainer_registry.items()
                        if k in enable_list}

    if disable_list:
        trainer_list = {v for k, v in trainer_registry.items()
                        if k not in trainer_list}

    return trainer_list


def train_from_configure(input_files_list, output_dir, configure_file):
    with open(configure_file) as fd:
        stream = fd.read()
        configure = yaml.load(stream)

    return train(input_files_list, output_dir, **configure)


def train(input_files_list, output_dir, **kwargs):
    trainer_list = get_trainer_list(**kwargs)
    trainer_instance_list = [i(**kwargs) for i in trainer_list]

    corpus = []
    for input_file in input_files_list:
        with open(input_file, encoding="utf-8") as fd:
            for raw_line in fd:
                line = raw_line.strip()

                if not line:
                    # skip empty line
                    continue

                token_list = line.split()

                corpus.append(token_list)

    for trainer_instance in trainer_instance_list:
        trainer_instance.train(corpus)
        trainer_instance.save(output_dir)
