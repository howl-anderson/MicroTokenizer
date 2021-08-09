from MicroTokenizer.tokenizers.ensemble.tokenizer import EnsembleTokenizer
from MicroTokenizer import dag_tokenizer


tokenizer = EnsembleTokenizer({"Han": dag_tokenizer})
tokens = tokenizer.segment("2021年时我在Korea的汉城听了이효리的にほんご这首歌。")
print(tokens)
