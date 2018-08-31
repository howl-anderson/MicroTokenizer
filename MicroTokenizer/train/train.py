from MicroTokenizer.train.registry import trainer_list


def train(input_files_list, output_dir):
    trainer_instance_list = [i() for i in trainer_list]

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
