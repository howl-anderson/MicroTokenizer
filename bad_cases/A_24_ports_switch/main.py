from MicroTokenizer.tokenizer import Tokenizer

tokenizer = Tokenizer()
tokenizer.init_dag_tokenizer()

tokenizer.dag_tokenizer.graph_builder.build_graph("二十四口交换机")
tokenizer.dag_tokenizer.graph_builder.write_graphml("output.graphml")
