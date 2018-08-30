from MicroTokenizer.tokenizer import Tokenizer

tokenizer = Tokenizer()
tokenizer.init_dag_tokenizer()

dag_tokenizer = tokenizer.dag_tokenizer
dag_tokenizer.graph_builder.build_graph("知识就是力量")
dag_tokenizer.graph_builder.write_graphml("output.graphml")
