import plac

from MicroTokenizer.train.train import train as train_func


# TODO: plac based CLI may have bug, need be checked
# TODO: Add configure file option for CRF feature function list
@plac.annotations(
    output_dir=("output directory to store model in", "positional", None, str),
    train_data=("location of training data", "positional",
                None, str, None, "n")
)
def train(output_dir, *train_data):
    train_func(train_data, output_dir)
