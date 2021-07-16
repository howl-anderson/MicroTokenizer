from MicroTokenizer.train.train import train_from_configure


def train(output_dir, train_data, configure_file=None):
    train_from_configure([train_data], output_dir, configure_file=configure_file)


if __name__ == "__main__":
    import plac
    print(plac.call(train))
