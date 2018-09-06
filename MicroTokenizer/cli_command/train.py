import plac

from MicroTokenizer.train.train import train


@plac.annotations(
    output_dir=("output directory to store model in", "positional", None, str),
    train_data=("location of training data", "positional",
                None, str, None, "n")
)
def train(output_dir, *train_data):
    train(train_data, output_dir)
