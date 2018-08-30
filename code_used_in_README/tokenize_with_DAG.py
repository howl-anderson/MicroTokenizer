from MicroTokenizer.tokenizer import Tokenizer

integrated_tokenizer = Tokenizer()
integrated_tokenizer.init_dag_tokenizer()

tokens = integrated_tokenizer.dag_tokenizer.segment("知识就是力量")
print(tokens)
