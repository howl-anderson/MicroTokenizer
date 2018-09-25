from joblib import Parallel, delayed
import yaml

from MicroTokenizer.train.registry import get_trainer_list


def train_from_configure(input_files_list, output_dir, configure_file):
    with open(configure_file) as fd:
        stream = fd.read()
        configure = yaml.load(stream)

    return train(input_files_list, output_dir, **configure)


def train(input_files_list, output_dir, **kwargs):
    trainer_list = get_trainer_list(**kwargs)
    trainer_instance_list = [i(**kwargs) for i in trainer_list]

    for input_file in input_files_list:
        with open(input_file) as fd:
            for raw_line in fd:
                line = raw_line.strip()

                if not line:
                    # skip empty line
                    continue

                token_list = line.split()

                for trainer_instance in trainer_instance_list:
                    trainer_instance.train_one_line(token_list)

    for trainer_instance in trainer_instance_list:
        trainer_instance.do_train()
        trainer_instance.persist_to_dir(output_dir)


def train_parallel(input_files_list, output_dir, **kwargs):
    trainer_list = get_trainer_list(**kwargs)
    trainer_instance_list = [i(**kwargs) for i in trainer_list]

    token_collection = []
    for input_file in input_files_list:
        with open(input_file) as fd:
            for raw_line in fd:
                line = raw_line.strip()

                if not line:
                    # skip empty line
                    continue

                token_list = line.split()

                token_collection.append(token_list)

    Parallel(n_jobs=-1)(
        delayed(train_tokenizer_from_collection)(
            trainer_instance, token_collection, output_dir
        )
        for trainer_instance in trainer_instance_list
    )


def train_tokenizer_from_collection(trainer_instance, token_collection, output_dir):
    for token_list in token_collection:
        trainer_instance.train_one_line(token_list)

    trainer_instance.do_train()
    trainer_instance.persist_to_dir(output_dir)
