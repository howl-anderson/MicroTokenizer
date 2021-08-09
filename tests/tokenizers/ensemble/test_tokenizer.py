from MicroTokenizer.tokenizers.ensemble.tokenizer import EnsembleTokenizer
from MicroTokenizer import dag_tokenizer


def test_tokenizer():
    tokenizer = EnsembleTokenizer({"Han": dag_tokenizer})
    result = tokenizer.segment("王小明在2021年的时候参加了TsingHua University的活动，并听了이효리的にほんご。")
    print(result)
