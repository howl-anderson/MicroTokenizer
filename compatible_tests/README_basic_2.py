import MicroTokenizer

MicroTokenizer.initialize()

from MicroTokenizer import default_tokenizer

dag_tokenizer = default_tokenizer.dag_tokenizer
dag_tokenizer.build_graph("知识就是力量")
dag_tokenizer.write_graphml("output.graphml")
