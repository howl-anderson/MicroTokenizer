import plac


@plac.annotations(
    output_dir=("output directory to store model in", "positional", None, str),
    train_data=("location of JSON-formatted training data", "positional",
                None, str)
)
def train(output_dir, train_data):
    pass
